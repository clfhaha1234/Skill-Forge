"""
Slide Generator — orchestrates the full PPT generation pipeline.

Pipeline (in order):
    1. LLM reads skill files + TASK_PROMPT.md + js_templates + constraints
       → writes pptxgenjs JavaScript to generate.js in the session output dir.
    2. Code patches are applied to the generated JS.
    3. `node generate.js` runs in the session output dir → produces slide.pptx.
    4. `soffice --headless --convert-to pdf slide.pptx` → slide.pdf.
    5. `pdftoppm -r 150 -jpeg -f 1 -l 1 slide.pdf slide` → slide-1.jpg (page 1).
    6. Returns the Path to slide-1.jpg.

Skill files are read from the session directory so that agent edits to
SKILL.md, editing.md, and pptxgenjs.md take effect. The repo copies are
only used as fallbacks if a file isn't in the session dir.

Session isolation:
    All generated artifacts (generate.js, slide.pptx, slide.pdf, slide-1.jpg)
    are written into a subdirectory of session_dir so that concurrent sessions
    do not share output paths.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import textwrap
from pathlib import Path

from google import genai
from google.genai import types

from models import SlideSkillState


REPO_ROOT = Path(__file__).parent.parent

# On macOS, LibreOffice installs to a .app bundle not on PATH by default.
_SOFFICE_MACOS = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
SOFFICE = shutil.which("soffice") or (_SOFFICE_MACOS if Path(_SOFFICE_MACOS).exists() else "soffice")

# On macOS, poppler (pdftoppm) is installed via Homebrew — check both
# Apple Silicon and Intel prefix locations.
PDFTOPPM = (
    shutil.which("pdftoppm")
    or ("/opt/homebrew/bin/pdftoppm" if Path("/opt/homebrew/bin/pdftoppm").exists() else None)
    or ("/usr/local/bin/pdftoppm" if Path("/usr/local/bin/pdftoppm").exists() else None)
    or "pdftoppm"
)

# Gemini Flash: fast and cost-effective for code generation.
GENERATOR_MODEL = "gemini-3-flash-preview"
GENERATOR_MAX_TOKENS = 4096


class SlideGenerator:
    """Drives the LLM → Node.js → LibreOffice → pdftoppm pipeline."""

    def __init__(
        self,
        task_prompt_path: Path,
        pptx_skill_dir: Path,
        reference_dir: Path,
    ) -> None:
        self.task_prompt = task_prompt_path.read_text(encoding="utf-8")
        self.pptx_skill_dir = pptx_skill_dir
        self.reference_dir = reference_dir
        self._client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    def generate(
        self,
        session_id: str,
        session_dir: Path,
        state: SlideSkillState | None = None,
    ) -> Path:
        """
        Run the full pipeline for one optimization step.

        Args:
            session_id: Used only for logging/naming.
            session_dir: Isolated directory containing the session's skill files.
            state: Session state with js_templates, constraints, code_patches.

        Returns:
            Absolute path to the generated slide JPG (slide-1.jpg).

        Raises:
            RuntimeError: If any pipeline stage (LLM, Node, LibreOffice,
                          pdftoppm) fails.
        """
        out_dir = session_dir / "output"
        out_dir.mkdir(exist_ok=True)

        js_path = out_dir / "generate.js"
        pptx_path = out_dir / "slide.pptx"
        jpg_stem = out_dir / "slide"
        jpg_path = out_dir / "slide-1.jpg"

        # Stage 1+2: LLM generates JS, patches applied, Node executes it.
        # Retry up to 3 times feeding Node errors back to the LLM.
        node_error: str | None = None
        for attempt in range(1, 4):
            js_code = self._call_generator_llm(
                session_dir, state=state, node_error=node_error,
            )

            # Apply code patches from the session state.
            if state and state.code_patches:
                js_code = self._apply_patches(js_code, state.code_patches)

            js_path.write_text(js_code, encoding="utf-8")
            try:
                self._run(["node", str(js_path)], cwd=out_dir, stage="node generate.js")
                node_error = None
                break
            except RuntimeError as exc:
                node_error = str(exc)
                if attempt == 3:
                    raise
        if not pptx_path.exists():
            raise RuntimeError(
                f"node generate.js completed but {pptx_path} was not created."
            )

        # Stage 3: LibreOffice converts .pptx → .pdf.
        self._run(
            [
                SOFFICE,
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                str(out_dir),
                str(pptx_path),
            ],
            cwd=out_dir,
            stage="soffice --convert-to pdf",
        )
        pdf_path = out_dir / "slide.pdf"
        if not pdf_path.exists():
            raise RuntimeError(
                f"LibreOffice completed but {pdf_path} was not created."
            )

        # Stage 4: pdftoppm converts PDF page 1 → JPG at 150 DPI.
        # Output: slide-1.jpg (pdftoppm appends "-{page}" automatically).
        self._run(
            [
                PDFTOPPM,
                "-r",
                "150",
                "-jpeg",
                "-f",
                "1",
                "-l",
                "1",  # only page 1
                str(pdf_path),
                str(jpg_stem),
            ],
            cwd=out_dir,
            stage="pdftoppm",
        )
        if not jpg_path.exists():
            raise RuntimeError(
                f"pdftoppm completed but {jpg_path} was not created."
            )

        return jpg_path

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _call_generator_llm(
        self,
        session_dir: Path,
        state: SlideSkillState | None = None,
        node_error: str | None = None,
    ) -> str:
        """
        Call the generator LLM with skill files + task prompt as context.

        Reads skill files from the session directory first (so agent edits
        take effect), falling back to the repo's pptx/ dir for any files
        not present in the session.

        Returns the raw JavaScript code string (without markdown fences).
        """
        design_rules = (session_dir / "DESIGN_RULES.md").read_text(encoding="utf-8")
        examples = (session_dir / "EXAMPLES.md").read_text(encoding="utf-8")

        # Load pptx tooling from session dir (edited copies) with fallback
        # to repo originals.
        pptx_skill = self._read_pptx_skill(session_dir)

        system_prompt = textwrap.dedent("""\
            You are an expert pptxgenjs developer. You will write a complete,
            runnable Node.js script that generates a PowerPoint slide using
            the pptxgenjs library.

            Rules:
            - Output ONLY the JavaScript code. No markdown fences, no explanation.
            - The script must save the file as "slide.pptx" in the current directory.
            - Follow the DESIGN_RULES.md and EXAMPLES.md exactly.
            - Use the pptxgenjs API reference below for correct method calls.
        """)

        user_message = textwrap.dedent(f"""\
            ## pptxgenjs API Reference
            {pptx_skill}

            ## Brand Style: DESIGN_RULES.md
            {design_rules}

            ## Brand Style: EXAMPLES.md
            {examples}

            ## Task
            {self.task_prompt}
        """)

        # Inject hard constraints if any.
        if state and state.constraints:
            constraints_text = "\n".join(f"- {c}" for c in state.constraints)
            user_message += textwrap.dedent(f"""
            ## Hard Constraints
            You MUST follow these constraints exactly:
            {constraints_text}
            """)

        # Inject JS templates if any.
        if state and state.js_templates:
            templates_text = ""
            for name, code in state.js_templates.items():
                templates_text += f"\n### {name}\n```javascript\n{code}\n```\n"
            user_message += textwrap.dedent(f"""
            ## Required Code Blocks
            You MUST include the following code blocks verbatim in your script.
            Do NOT modify them — copy them exactly as shown:
            {templates_text}
            """)

        user_message += "\nWrite the complete pptxgenjs JavaScript file now.\n"

        if node_error:
            user_message += textwrap.dedent(f"""

            ## Previous attempt failed — fix these errors
            Your previous script produced the following Node.js error.
            Rewrite the script and fix the issue:

            {node_error}
        """)

        response = self._client.models.generate_content(
            model=GENERATOR_MODEL,
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                max_output_tokens=GENERATOR_MAX_TOKENS,
            ),
        )

        code = response.text.strip()

        # Extract from markdown code fence if present (LLMs often add them
        # despite instructions). Handles ```javascript, ```js, or plain ```.
        fence_match = re.search(r"```(?:javascript|js)?\n(.*?)```", code, re.DOTALL)
        if fence_match:
            code = fence_match.group(1).strip()

        # Rewrite all bare require('pkg') calls to absolute paths so the
        # script works when run from any /tmp/ directory.  We only rewrite
        # packages that actually exist in node_modules; unknown packages are
        # left untouched (they'd fail at runtime but at least not silently).
        node_modules = REPO_ROOT / "node_modules"

        def _rewrite_require(m: re.Match) -> str:
            quote = m.group(1)
            pkg = m.group(2)
            pkg_path = node_modules / pkg
            if pkg_path.exists():
                return f"require({quote}{pkg_path}{quote})"
            return m.group(0)  # leave unknown packages as-is

        code = re.sub(r"require\((['\"])([^./][^'\"]*)\1\)", _rewrite_require, code)

        # LLMs sometimes emit the require line twice. Keep only the first
        # declaration to avoid "Identifier already declared" SyntaxError.
        seen: set[str] = set()
        deduped = []
        for line in code.splitlines():
            m = re.search(r"require\(['\"]([^'\"]+)['\"]\)", line)
            if m and "node_modules" in line:
                pkg = m.group(1)
                if pkg in seen:
                    continue
                seen.add(pkg)
            deduped.append(line)
        code = "\n".join(deduped)

        return code

    def _read_pptx_skill(self, session_dir: Path) -> str:
        """
        Concatenate the pptx skill files for LLM context.

        Reads from session_dir first (agent-edited copies), falling back
        to the repo's pptx/ dir for files not yet copied or edited.
        """
        parts = []
        for fname in ("SKILL.md", "editing.md", "pptxgenjs.md"):
            session_copy = session_dir / fname
            repo_copy = self.pptx_skill_dir / fname
            if session_copy.exists():
                parts.append(f"### {fname}\n{session_copy.read_text(encoding='utf-8')}")
            elif repo_copy.exists():
                parts.append(f"### {fname}\n{repo_copy.read_text(encoding='utf-8')}")
        return "\n\n".join(parts)

    @staticmethod
    def _apply_patches(code: str, patches: list[dict[str, str]]) -> str:
        """Apply regex find/replace patches to generated JS code."""
        for patch in patches:
            code = re.sub(patch["pattern"], patch["replacement"], code)
        return code

    @staticmethod
    def _run(cmd: list[str], cwd: Path, stage: str) -> None:
        """Run a subprocess; raise RuntimeError with context if it fails."""
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 min hard limit per stage
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"Pipeline stage '{stage}' failed (exit {result.returncode}).\n"
                f"stdout: {result.stdout[-2000:]}\n"
                f"stderr: {result.stderr[-2000:]}"
            )
