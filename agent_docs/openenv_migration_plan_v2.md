# OpenEnv Migration Plan v2 — Skill Forge → OpenEnv Environment

**Date**: 2026-03-07
**Status**: Implementation-ready
**Target**: HuggingFace Spaces (OpenEnv-compatible)

---

## 1. Overview

Skill Forge is a self-improving PowerPoint generation loop that, starting from a minimal brand-style baseline, iteratively improves a McKinsey-style slide by evolving two skill files. The loop reached 89/100 in 5 iterations.

**What is being optimized**: Two brand/task-specific files — `DESIGN_RULES.md` and `EXAMPLES.md` — that guide an LLM's pptxgenjs code generation. These files encode McKinsey visual design rules (color palette, typography, structural elements) and accumulated example guidance.

**What is NOT being optimized**: The generic pptx tooling skill in `pptx/` (SKILL.md, editing.md, pptxgenjs.md). These files define how the agent-as-executor uses pptxgenjs and remain unchanged across all optimization rounds.

**What OpenEnv adds**: A standardized environment interface so that any RL/optimization agent can drive the Skill Forge loop without knowing its internals. The environment exposes `reset()`, `step(action)`, and `observe()` via a gRPC/HTTP server defined by the OpenEnv protocol.

**Full generation pipeline per step**:

```
Agent issues action (edit skill files)
        ↓
skill_manager.py applies edit to isolated session directory
        ↓
slide_generator.py: LLM reads DESIGN_RULES.md + EXAMPLES.md + TASK_PROMPT.md
        → writes JavaScript (pptxgenjs)
        ↓
node generate.js → slide.pptx
        ↓
soffice --headless --convert-to pdf slide.pptx
        ↓
pdftoppm -r 150 slide.pdf slide → slide-1.jpg
        ↓
evaluator.py: Claude Opus 4.6 + vision → scores JSON
        ↓
Observation returned to agent
```

Each step takes approximately 60–120 seconds (two LLM API calls + Node.js + LibreOffice). At `max_steps=10` an episode runs 10–20 minutes. For HuggingFace Spaces with resource constraints, **5–7 steps per episode is more realistic**.

---

## 2. Conceptual Clarification

Understanding which files are "the skill" is critical. There are two distinct layers:

### Layer 1 — Generic pptx Agent Tooling (`pptx/`)

These files live in `pptx/` and are maintained by Anthropic. They teach the LLM agent *how to use pptxgenjs as a tool* — the API, shape types, coordinate systems, etc. They are analogous to a standard library: stable, versioned independently, and not task-specific.

```
pptx/
├── SKILL.md         # pptxgenjs capability overview and agent instructions
├── editing.md       # Shape editing primitives and patterns
└── pptxgenjs.md     # Full pptxgenjs API reference
```

**These files are read by the agent-as-executor (the slide generator LLM). They are NEVER the target of optimization.**

### Layer 2 — Evolving Brand Style Files (the "skill" being optimized)

These files live in `skill_v{N}/` and encode McKinsey-specific visual design knowledge:

```
skill_v0/
├── DESIGN_RULES.md  # Color palette, typography, layout coords, structural elements
└── EXAMPLES.md      # Accumulated guidance from prior optimization rounds
```

The optimizer LLM reads `DESIGN_RULES.md + EXAMPLES.md + evaluation feedback` and rewrites or edits these files to produce `skill_v{N+1}/`. The agent environment manages this evolution loop.

**Key invariant**: `DESIGN_RULES.md` and `EXAMPLES.md` are the only files the optimizer modifies. The pptx/ tooling files are read-only context for the generator.

### The Baseline

The baseline is `skill_v0/` — minimal initial style guidelines with an empty EXAMPLES.md. It must be committed to the repo as `skill_files_baseline/` and represents the true starting point, not any evolved version. On environment `reset()`, the session's skill files are restored to this baseline.

---

## 3. Project Structure

```
pptx-skillforge-hackathon/
├── package.json                    # pptxgenjs ^4.0.1 dependency
├── pyproject.toml                  # Python package definition
│
├── pptx/                           # Generic pptx agent tooling — DO NOT MODIFY
│   ├── SKILL.md
│   ├── editing.md
│   └── pptxgenjs.md
│
├── skill_files_baseline/           # Committed minimal baseline (skill_v0 content)
│   ├── DESIGN_RULES.md             # Minimal McKinsey rules, no teal/wrong colors
│   └── EXAMPLES.md                 # Empty: "(Empty — no prior optimization rounds)"
│
├── output/
│   ├── TASK_PROMPT.md              # Fixed task (Dutch Hydrogen Strategy)
│   ├── evaluator.py                # Original standalone evaluator (unchanged)
│   ├── reference/
│   │   ├── ref-01.jpg              # Cover page reference
│   │   ├── ref-02.jpg              # Content page reference
│   │   ├── ref-03.jpg              # Data/chart page reference
│   │   ├── ref-04.jpg              # Data/chart page reference
│   │   └── ref-05.jpg              # Content page reference
│   ├── skill_v0/ … skill_v5/       # Historical optimization rounds
│   ├── generate_v0.js … v5.js      # Historical generated JS files
│   └── slide_v0.pptx … v5.pptx + JPGs
│
└── openenv/                        # OpenEnv environment package
    ├── app.py                      # FastAPI server entry point
    ├── client.py                   # Reference client implementation
    ├── openenv.yaml                # OpenEnv manifest
    ├── Dockerfile
    ├── models.py                   # Pydantic data models
    ├── slide_skill_environment.py  # Core environment logic
    ├── skill_manager.py            # Skill file I/O + apply actions
    ├── slide_generator.py          # Full pipeline: LLM → JS → .pptx → JPG
    └── evaluator_adapter.py        # Adapter wrapping output/evaluator.py logic
```

---

## 4. Data Models

`openenv/models.py`

```python
"""
Pydantic data models for the Slide Skill OpenEnv environment.

Action space:
    SlideSkillAction is a discriminated union of two action types:
    - EditSectionAction: Replace a named section's body in one skill file.
    - ReplaceFileAction: Replace the entire content of one skill file.

    EditSectionAction is appropriate when the agent wants surgical edits
    (e.g., update only the typography section). ReplaceFileAction is used
    when the optimizer rewrites the file wholesale, which is what the
    historical optimizer LLM actually does.

Observation space:
    SlideSkillObservation contains the full evaluator output including all
    seven score dimensions plus qualitative feedback fields.
"""

from __future__ import annotations

from typing import Annotated, Literal, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------

SkillFile = Literal["DESIGN_RULES.md", "EXAMPLES.md"]
"""The two skill files the optimizer is allowed to modify."""


class EditSectionAction(BaseModel):
    """
    Replace the body of a named markdown section within a skill file.

    The section is identified by its heading text (without the leading #
    characters). The replacement spans from immediately after the heading
    line to (but not including) the next heading of equal or higher level.

    Example:
        action = EditSectionAction(
            file="DESIGN_RULES.md",
            section_heading="Color Palette",
            new_body="- Navy (#0C2340): primary\\n- White: background\\n"
        )
    """

    action_type: Literal["edit_section"] = "edit_section"
    file: SkillFile = Field(..., description="Which skill file to edit.")
    section_heading: str = Field(
        ...,
        description=(
            "Exact heading text (without leading # markers). "
            "Case-sensitive. Must match a heading in the file."
        ),
    )
    new_body: str = Field(
        ...,
        description="New markdown content for the section body (after the heading line).",
    )


class ReplaceFileAction(BaseModel):
    """
    Replace the entire content of a skill file.

    Use this when the optimizer rewrites the file wholesale rather than
    making targeted section edits. This is the mode used by the historical
    optimizer LLM in the Skill Forge loop.
    """

    action_type: Literal["replace_file"] = "replace_file"
    file: SkillFile = Field(..., description="Which skill file to replace.")
    new_content: str = Field(
        ...,
        description="Complete new file content (valid markdown).",
    )


# Discriminated union — action_type is the discriminator field.
SlideSkillAction = Annotated[
    EditSectionAction | ReplaceFileAction,
    Field(discriminator="action_type"),
]


# ---------------------------------------------------------------------------
# Scores
# ---------------------------------------------------------------------------

class SlideScores(BaseModel):
    """Raw scores from the McKinsey evaluator. Each dimension is 0–15 except
    overall_impression which is 0–10. Total is 0–100."""

    background_layout: int = Field(..., ge=0, le=15)
    color_palette: int = Field(..., ge=0, le=15)
    typography: int = Field(..., ge=0, le=15)
    title_quality: int = Field(..., ge=0, le=15)
    data_presentation: int = Field(..., ge=0, le=15)
    structural_elements: int = Field(..., ge=0, le=15)
    overall_impression: int = Field(..., ge=0, le=10)

    @property
    def total(self) -> int:
        return (
            self.background_layout
            + self.color_palette
            + self.typography
            + self.title_quality
            + self.data_presentation
            + self.structural_elements
            + self.overall_impression
        )


# ---------------------------------------------------------------------------
# Observation
# ---------------------------------------------------------------------------

class SlideSkillObservation(BaseModel):
    """
    Observation returned to the agent after each step.

    Contains the full evaluator output so the optimizer LLM has all the
    information it needs to write the next skill revision: numeric scores,
    qualitative strengths/weaknesses, and the one-line verdict.
    """

    scores: SlideScores
    total: int = Field(..., description="Sum of all score dimensions (0–100).")
    strengths: list[str] = Field(
        default_factory=list,
        description="List of what the slide does well, from the evaluator.",
    )
    weaknesses: list[str] = Field(
        default_factory=list,
        description="List of what needs improvement, from the evaluator.",
    )
    one_line_verdict: str = Field(
        ..., description="Single-sentence summary from the evaluator."
    )
    reward: float = Field(
        ...,
        description=(
            "Score delta vs. previous step, capped to [-0.3, +0.3] and "
            "normalized to [-1.0, +1.0] by dividing by 100. "
            "Capping reduces reward noise from LLM evaluation variance."
        ),
    )
    step: int = Field(..., description="Current step index (0-based).")
    done: bool = Field(..., description="True if max_steps reached.")
    # Paths are strings for JSON serialization
    jpg_path: str = Field(
        ..., description="Absolute path to the generated slide JPG."
    )
    design_rules_content: str = Field(
        ...,
        description="Current DESIGN_RULES.md content (after action was applied).",
    )
    examples_content: str = Field(
        ...,
        description="Current EXAMPLES.md content (after action was applied).",
    )


# ---------------------------------------------------------------------------
# State (internal, not exposed to client)
# ---------------------------------------------------------------------------

class SlideSkillState(BaseModel):
    """Internal environment state. Not serialized to the client."""

    session_id: str
    step: int = 0
    prev_total: int = 0  # score from the previous step (for reward calculation)
    session_dir: str = Field(
        ...,
        description=(
            "Absolute path to the isolated session directory under /tmp/. "
            "Contains copies of DESIGN_RULES.md and EXAMPLES.md that this "
            "session is free to modify without affecting other sessions."
        ),
    )
```

---

## 5. Environment Logic

`openenv/slide_skill_environment.py`

```python
"""
Slide Skill Environment — OpenEnv-compatible environment for optimizing
McKinsey-style PowerPoint slide generation.

Concurrency model:
    SUPPORTS_CONCURRENT_SESSIONS = True

    Each session gets an isolated working directory at /tmp/slide_skill_{session_id}/.
    Skill files (DESIGN_RULES.md, EXAMPLES.md) are copied there on reset() and
    modified in place during the session. The shared repo files are never modified.
    This means multiple sessions can run simultaneously without file conflicts.

    The only shared resource is the Anthropic API key, which is rate-limited
    per-account. For HuggingFace Spaces, running 2-3 concurrent sessions is
    realistic before hitting rate limits.

Episode timing:
    Each step involves two LLM calls (generator + evaluator) plus Node.js and
    LibreOffice. Expect 60–120 seconds per step. At max_steps=7, a full episode
    runs 7–14 minutes.

Reward function:
    reward = clip(total_score - prev_total_score, -30, +30) / 100
    Capping at ±30 points (±0.3 reward) dampens LLM evaluation noise. A score
    can fluctuate ±5–10 points between identical slides due to evaluator variance,
    so capping prevents large undeserved penalties or bonuses.
"""

from __future__ import annotations

import shutil
import uuid
from pathlib import Path
from typing import ClassVar

from models import (
    SlideSkillAction,
    SlideSkillObservation,
    SlideSkillState,
    SlideScores,
)
from skill_manager import SkillManager
from slide_generator import SlideGenerator
from evaluator_adapter import EvaluatorAdapter


# Paths relative to repo root — adjust if the package moves.
REPO_ROOT = Path(__file__).parent.parent
BASELINE_DIR = REPO_ROOT / "skill_files_baseline"
TASK_PROMPT_PATH = REPO_ROOT / "output" / "TASK_PROMPT.md"
REFERENCE_DIR = REPO_ROOT / "output" / "reference"

# Reward capping parameters
REWARD_CLIP_POINTS = 30   # clip score delta to ±30 before normalizing
REWARD_SCALE = 100.0      # divide clipped delta by this to get [-0.3, +0.3]

MAX_STEPS = 7


class SlideSkillEnvironment:
    """OpenEnv environment for the Skill Forge optimization loop."""

    SUPPORTS_CONCURRENT_SESSIONS: ClassVar[bool] = True

    def __init__(self) -> None:
        self._sessions: dict[str, SlideSkillState] = {}
        self._generator = SlideGenerator(
            task_prompt_path=TASK_PROMPT_PATH,
            pptx_skill_dir=REPO_ROOT / "pptx",
            reference_dir=REFERENCE_DIR,
        )
        self._evaluator = EvaluatorAdapter(reference_dir=REFERENCE_DIR)

    # ------------------------------------------------------------------
    # Public OpenEnv interface
    # ------------------------------------------------------------------

    def reset(self, session_id: str | None = None) -> str:
        """
        Initialize or reinitialize a session.

        Creates an isolated working directory under /tmp/ and copies the
        baseline skill files into it. Returns the session_id.
        """
        session_id = session_id or str(uuid.uuid4())

        session_dir = Path(f"/tmp/slide_skill_{session_id}")
        if session_dir.exists():
            shutil.rmtree(session_dir)
        session_dir.mkdir(parents=True)

        # Copy baseline skill files into the session directory.
        for fname in ("DESIGN_RULES.md", "EXAMPLES.md"):
            src = BASELINE_DIR / fname
            if not src.exists():
                raise FileNotFoundError(
                    f"Baseline file missing: {src}. "
                    "Commit skill_files_baseline/ to the repo."
                )
            shutil.copy2(src, session_dir / fname)

        self._sessions[session_id] = SlideSkillState(
            session_id=session_id,
            step=0,
            prev_total=0,
            session_dir=str(session_dir),
        )
        return session_id

    def step(self, session_id: str, action: SlideSkillAction) -> SlideSkillObservation:
        """
        Apply an action, run the generation pipeline, evaluate, and return
        an observation.

        Args:
            session_id: Must be a live session (call reset() first).
            action: Either EditSectionAction or ReplaceFileAction.

        Returns:
            SlideSkillObservation with scores, feedback, reward, and file contents.

        Raises:
            KeyError: If session_id is not found.
            RuntimeError: If the generation or evaluation pipeline fails.
        """
        state = self._sessions[session_id]
        session_dir = Path(state.session_dir)

        # 1. Apply the action to the session's skill files.
        manager = SkillManager(session_dir)
        manager.apply(action)

        # 2. Run the full generation pipeline.
        jpg_path = self._generator.generate(
            session_id=session_id,
            session_dir=session_dir,
        )

        # 3. Evaluate the generated slide.
        eval_result = self._evaluator.evaluate(jpg_path)

        # 4. Compute reward (capped score delta).
        delta = eval_result["total"] - state.prev_total
        clipped_delta = max(-REWARD_CLIP_POINTS, min(REWARD_CLIP_POINTS, delta))
        reward = clipped_delta / REWARD_SCALE

        # 5. Update state.
        state.step += 1
        state.prev_total = eval_result["total"]
        done = state.step >= MAX_STEPS

        # 6. Read back current file contents for the observation.
        design_rules = (session_dir / "DESIGN_RULES.md").read_text()
        examples = (session_dir / "EXAMPLES.md").read_text()

        scores = SlideScores(**eval_result["scores"])

        return SlideSkillObservation(
            scores=scores,
            total=eval_result["total"],
            strengths=eval_result.get("strengths", []),
            weaknesses=eval_result.get("weaknesses", []),
            one_line_verdict=eval_result["one_line_verdict"],
            reward=reward,
            step=state.step,
            done=done,
            jpg_path=str(jpg_path),
            design_rules_content=design_rules,
            examples_content=examples,
        )

    def close(self, session_id: str) -> None:
        """Clean up session resources. Deletes the /tmp/ session directory."""
        if session_id in self._sessions:
            state = self._sessions.pop(session_id)
            session_dir = Path(state.session_dir)
            if session_dir.exists():
                shutil.rmtree(session_dir)
```

---

## 6. Supporting Modules

### 6a. Skill Manager

`openenv/skill_manager.py`

```python
"""
Skill file manager — applies actions to an isolated session directory.

Operates exclusively on files within session_dir (a /tmp/ path).
Never touches the repo's baseline or any shared files.

Section editing rules:
    A "section" is a markdown heading of any level (# to ######).
    EditSectionAction finds the first heading whose text matches
    section_heading (case-sensitive, stripped), then replaces everything
    from the line after that heading up to (but not including) the next
    heading of equal or higher level (i.e., same or fewer # characters).
    If no next heading is found, the replacement extends to end-of-file.
"""

from __future__ import annotations

import re
from pathlib import Path

from models import EditSectionAction, ReplaceFileAction, SlideSkillAction


class SkillManager:
    """Manages DESIGN_RULES.md and EXAMPLES.md within a session directory."""

    def __init__(self, session_dir: Path) -> None:
        self.session_dir = session_dir

    def apply(self, action: SlideSkillAction) -> None:
        """
        Dispatch to the appropriate handler based on action type.

        Raises:
            ValueError: If action_type is unrecognized or section not found.
            FileNotFoundError: If the target skill file does not exist.
        """
        target = self.session_dir / action.file
        if not target.exists():
            raise FileNotFoundError(f"Skill file not found in session: {target}")

        if action.action_type == "replace_file":
            self._replace_file(target, action)
        elif action.action_type == "edit_section":
            self._edit_section(target, action)
        else:
            raise ValueError(f"Unknown action_type: {action.action_type!r}")

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _replace_file(target: Path, action: ReplaceFileAction) -> None:
        """Overwrite the entire file with new_content."""
        target.write_text(action.new_content, encoding="utf-8")

    @staticmethod
    def _edit_section(target: Path, action: EditSectionAction) -> None:
        """Replace the body of a named markdown section."""
        text = target.read_text(encoding="utf-8")
        lines = text.splitlines(keepends=True)

        # Find the heading line.
        heading_pattern = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
        heading_idx: int | None = None
        heading_level: int = 0

        for i, line in enumerate(lines):
            m = heading_pattern.match(line.rstrip("\n\r"))
            if m and m.group(2) == action.section_heading:
                heading_idx = i
                heading_level = len(m.group(1))
                break

        if heading_idx is None:
            raise ValueError(
                f"Section heading {action.section_heading!r} not found in {target.name}."
            )

        # Find where the section body ends (next heading of equal or higher level).
        end_idx = len(lines)
        for i in range(heading_idx + 1, len(lines)):
            m = heading_pattern.match(lines[i].rstrip("\n\r"))
            if m and len(m.group(1)) <= heading_level:
                end_idx = i
                break

        # Reconstruct the file.
        new_body = action.new_body
        if new_body and not new_body.endswith("\n"):
            new_body += "\n"

        new_lines = (
            lines[: heading_idx + 1]  # heading itself
            + [new_body]
            + lines[end_idx:]         # rest of file after the section
        )
        target.write_text("".join(new_lines), encoding="utf-8")

    def read_file(self, filename: str) -> str:
        """Read a skill file from the session directory."""
        return (self.session_dir / filename).read_text(encoding="utf-8")
```

### 6b. Slide Generator

`openenv/slide_generator.py`

```python
"""
Slide Generator — orchestrates the full PPT generation pipeline.

Pipeline (in order):
    1. LLM reads DESIGN_RULES.md + EXAMPLES.md + TASK_PROMPT.md + pptx/ tooling
       → writes pptxgenjs JavaScript to generate.js in the session output dir.
    2. `node generate.js` runs in the session output dir → produces slide.pptx.
    3. `soffice --headless --convert-to pdf slide.pptx` → slide.pdf.
    4. `pdftoppm -r 150 slide.pdf slide` → slide-1.jpg (page 1).
    5. Returns the Path to slide-1.jpg.

The generator LLM receives the pptx/ tooling files as context so it knows
the full pptxgenjs API — but those files are read-only; they are never
written to or returned in the observation.

Session isolation:
    All generated artifacts (generate.js, slide.pptx, slide.pdf, slide-1.jpg)
    are written into a subdirectory of session_dir so that concurrent sessions
    do not share output paths.
"""

from __future__ import annotations

import subprocess
import textwrap
from pathlib import Path

import anthropic


# The generator uses a capable coding model. Claude Sonnet is a good balance
# between quality and speed/cost for code generation.
GENERATOR_MODEL = "claude-sonnet-4-6"
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
        self._client = anthropic.Anthropic()

    def generate(self, session_id: str, session_dir: Path) -> Path:
        """
        Run the full pipeline for one optimization step.

        Args:
            session_id: Used only for logging/naming.
            session_dir: Isolated directory containing the session's
                         DESIGN_RULES.md and EXAMPLES.md.

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

        # Stage 1: LLM generates pptxgenjs JavaScript.
        js_code = self._call_generator_llm(session_dir)
        js_path.write_text(js_code, encoding="utf-8")

        # Stage 2: Node.js executes the JS to produce the .pptx file.
        self._run(
            ["node", str(js_path)],
            cwd=out_dir,
            stage="node generate.js",
        )
        if not pptx_path.exists():
            raise RuntimeError(
                f"node generate.js completed but {pptx_path} was not created."
            )

        # Stage 3: LibreOffice converts .pptx → .pdf.
        self._run(
            [
                "soffice",
                "--headless",
                "--convert-to", "pdf",
                "--outdir", str(out_dir),
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
                "pdftoppm",
                "-r", "150",
                "-jpeg",
                "-f", "1", "-l", "1",   # only page 1
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

    def _call_generator_llm(self, session_dir: Path) -> str:
        """
        Call the generator LLM with skill files + task prompt as context.

        Returns the raw JavaScript code string (without markdown fences).
        """
        design_rules = (session_dir / "DESIGN_RULES.md").read_text(encoding="utf-8")
        examples = (session_dir / "EXAMPLES.md").read_text(encoding="utf-8")

        # Load the generic pptx tooling files as executor context.
        pptx_skill = self._read_pptx_skill()

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

            Write the complete pptxgenjs JavaScript file now.
        """)

        response = self._client.messages.create(
            model=GENERATOR_MODEL,
            max_tokens=GENERATOR_MAX_TOKENS,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )

        code = response.content[0].text.strip()

        # Strip markdown code fences if the LLM added them despite instructions.
        if code.startswith("```"):
            code = code.split("\n", 1)[1]
            if code.endswith("```"):
                code = code.rsplit("```", 1)[0]
            code = code.strip()

        return code

    def _read_pptx_skill(self) -> str:
        """Concatenate the generic pptx skill files for LLM context."""
        parts = []
        for fname in ("SKILL.md", "editing.md", "pptxgenjs.md"):
            p = self.pptx_skill_dir / fname
            if p.exists():
                parts.append(f"### {fname}\n{p.read_text(encoding='utf-8')}")
        return "\n\n".join(parts)

    @staticmethod
    def _run(cmd: list[str], cwd: Path, stage: str) -> None:
        """Run a subprocess; raise RuntimeError with context if it fails."""
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300,   # 5 min hard limit per stage
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"Pipeline stage '{stage}' failed (exit {result.returncode}).\n"
                f"stdout: {result.stdout[-2000:]}\n"
                f"stderr: {result.stderr[-2000:]}"
            )
```

### 6c. Evaluator Adapter

`openenv/evaluator_adapter.py`

```python
"""
Evaluator Adapter — wraps the existing output/evaluator.py logic as a
reusable module with a clean interface.

This module does NOT import output/evaluator.py (which has a __main__ guard
and hardcoded paths). Instead, it re-implements the core evaluate_slide()
logic with:
    - Configurable reference image paths
    - A return type that includes all seven score keys, strengths, weaknesses,
      and one_line_verdict
    - No file I/O side effects (no evaluation_results.json written)

The evaluation prompt is identical to output/evaluator.py so scores are
comparable across the historical runs and the OpenEnv loop.
"""

from __future__ import annotations

import base64
import json
from pathlib import Path

import anthropic


# Must match output/evaluator.py exactly so historical scores are comparable.
EVALUATION_SYSTEM_PROMPT = """You are an expert McKinsey & Company slide design evaluator.

You will be shown:
1. REFERENCE IMAGES: 5 pages from a real McKinsey & Company consulting deck (Chilean Hydrogen Pathway, December 2020). These represent the gold standard for visual style.
2. CANDIDATE SLIDE: A programmatically generated PowerPoint slide about Dutch Hydrogen Strategy, rendered as a JPEG image.

Your job: Score how closely the CANDIDATE SLIDE matches the McKinsey visual style shown in the REFERENCE IMAGES.

## Scoring Rubric (100 points total)

### 1. Background & Base Layout (0-15 points)
- McKinsey content/data slides use WHITE backgrounds (dark navy is ONLY for section dividers/covers)
- Clean margins (~0.5" all sides)
- No unnecessary visual clutter
- 15: White bg, clean margins, professional spacing
- 10: White bg but spacing issues
- 5: Wrong background color or major layout problems
- 0: Completely wrong base (e.g., dark bg for data slide)

### 2. Color Palette Fidelity (0-15 points)
- McKinsey uses a RESTRAINED palette: navy/dark blue (#0C2340-ish), white, light greys
- Accent colors are used SPARINGLY — typically just 1-2 accent colors max
- NO rainbow effects, no bright multi-color schemes
- Crimson/red used only for thin divider lines, not large elements
- 15: Matches McKinsey's restrained navy/white/grey palette perfectly
- 10: Mostly correct but 1-2 color choices off
- 5: Too many colors or wrong color family
- 0: Completely different color scheme

### 3. Typography (0-15 points)
- Title: Large, bold, black or very dark, left-aligned (Georgia or similar serif for titles)
- Body: Clean sans-serif (Calibri-like), smaller, grey or dark grey
- Clear size hierarchy: title >> subtitle >> body >> footnotes
- No decorative fonts
- 15: Perfect type hierarchy matching McKinsey
- 10: Good hierarchy but font choices slightly off
- 5: Weak hierarchy or wrong fonts
- 0: No clear hierarchy

### 4. Title Quality — "So-What" Style (0-15 points)
- McKinsey titles state a CONCLUSION or INSIGHT, not just a topic
- GOOD: "The Netherlands aims to become Europe's green hydrogen hub, scaling from 500 MW to 3-4 GW by 2030"
- BAD: "Dutch Hydrogen Strategy (2020-2035)" or "Roadmap Overview"
- The title should tell you the key takeaway without reading the slide
- 15: Clear insight-driven conclusion title
- 10: Partial insight (has some specifics but reads more like a topic)
- 5: Pure topic label
- 0: Generic or missing title

### 5. Data Presentation (0-15 points)
- McKinsey uses structured TABLES for data (not floating stat callouts)
- Tables have: navy header borders (top + bottom of header row), light grey row dividers, bold left column labels
- Data should be organized, scannable, center-aligned values
- Key columns/years may be subtly highlighted
- 15: Clean structured table matching McKinsey format
- 10: Has data but format doesn't match McKinsey tables
- 5: Data present but poorly structured (floating callouts, inconsistent format)
- 0: No supporting data

### 6. Structural Elements (0-15 points)
- Thin crimson/red divider line below title area (not touching title — separated by whitespace)
- McKinsey footer: thin rule line + source text (left) + "McKinsey & Company" bold (right) + page number
- Numbered footnotes for data disclaimers
- Source attribution line
- 15: All structural elements present and correctly placed
- 10: Most elements present, minor placement issues
- 5: Missing 2+ structural elements
- 0: No McKinsey structural elements

### 7. Overall Visual Impression (0-10 points)
- Does this FEEL like it came from McKinsey?
- Would a consulting professional find this polished and credible?
- Is it clean, restrained, and authoritative — or busy, colorful, and amateur?
- 10: Indistinguishable from real McKinsey output
- 7: Close but a trained eye spots differences
- 4: Clearly generated/templated but has some McKinsey DNA
- 1: Does not resemble McKinsey at all

## Output Format

Return ONLY a JSON object with this exact structure (no markdown, no code fences):
{
    "scores": {
        "background_layout": <0-15>,
        "color_palette": <0-15>,
        "typography": <0-15>,
        "title_quality": <0-15>,
        "data_presentation": <0-15>,
        "structural_elements": <0-15>,
        "overall_impression": <0-10>
    },
    "total": <sum of all scores, 0-100>,
    "strengths": ["<strength 1>", "<strength 2>", ...],
    "weaknesses": ["<weakness 1>", "<weakness 2>", ...],
    "one_line_verdict": "<one sentence summary>"
}
"""

EVALUATOR_MODEL = "claude-opus-4-6"


def _encode_image(path: Path) -> dict:
    """Encode an image file to base64 for the Anthropic messages API."""
    data = base64.standard_b64encode(path.read_bytes()).decode("utf-8")
    suffix = path.suffix.lower()
    media_type = "image/jpeg" if suffix in (".jpg", ".jpeg") else "image/png"
    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": media_type,
            "data": data,
        },
    }


class EvaluatorAdapter:
    """
    Adapter that evaluates a generated slide JPG against McKinsey references.

    Uses the same Claude Opus 4.6 + vision approach as output/evaluator.py,
    but as a reusable class rather than a script with side effects.
    """

    REFERENCE_FILENAMES = [
        "ref-01.jpg",
        "ref-02.jpg",
        "ref-03.jpg",
        "ref-04.jpg",
        "ref-05.jpg",
    ]

    def __init__(self, reference_dir: Path) -> None:
        """
        Args:
            reference_dir: Directory containing ref-01.jpg through ref-05.jpg.
        """
        self.reference_dir = reference_dir
        self._client = anthropic.Anthropic()

        # Validate reference images exist at construction time.
        missing = [
            f for f in self.REFERENCE_FILENAMES
            if not (reference_dir / f).exists()
        ]
        if missing:
            raise FileNotFoundError(
                f"Missing reference images in {reference_dir}: {missing}"
            )

    def evaluate(self, slide_jpg_path: Path) -> dict:
        """
        Evaluate a generated slide against the McKinsey reference images.

        Args:
            slide_jpg_path: Absolute path to the slide JPG to evaluate.

        Returns:
            dict with keys:
                "scores": dict mapping the 7 dimension names to int scores
                "total": int, sum of all scores (0-100)
                "strengths": list[str]
                "weaknesses": list[str]
                "one_line_verdict": str

        Raises:
            FileNotFoundError: If slide_jpg_path does not exist.
            json.JSONDecodeError: If the LLM returns malformed JSON.
            RuntimeError: If the API call fails.
        """
        if not slide_jpg_path.exists():
            raise FileNotFoundError(f"Slide JPG not found: {slide_jpg_path}")

        content: list[dict] = []

        # Reference images first.
        content.append({
            "type": "text",
            "text": (
                "## REFERENCE IMAGES (Real McKinsey deck)\n"
                "The following 5 images are from a real McKinsey & Company consulting "
                "report. Study their visual style carefully."
            ),
        })
        for i, fname in enumerate(self.REFERENCE_FILENAMES, 1):
            ref_path = self.reference_dir / fname
            content.append(_encode_image(ref_path))
            content.append({"type": "text", "text": f"(Reference page {i})"})

        # Candidate slide.
        content.append({
            "type": "text",
            "text": (
                f"\n## CANDIDATE SLIDE TO EVALUATE\n"
                f"This is the generated slide: {slide_jpg_path.name}"
            ),
        })
        content.append(_encode_image(slide_jpg_path))
        content.append({
            "type": "text",
            "text": (
                "\nNow score this candidate slide against the McKinsey reference "
                "using the rubric. Return ONLY the JSON object."
            ),
        })

        response = self._client.messages.create(
            model=EVALUATOR_MODEL,
            max_tokens=1024,
            system=EVALUATION_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": content}],
        )

        text = response.content[0].text.strip()

        # Strip markdown code fences if present (LLMs sometimes add them
        # despite explicit instructions not to).
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        result = json.loads(text)

        # Validate required keys are present.
        required_score_keys = {
            "background_layout", "color_palette", "typography",
            "title_quality", "data_presentation", "structural_elements",
            "overall_impression",
        }
        missing_keys = required_score_keys - set(result.get("scores", {}).keys())
        if missing_keys:
            raise ValueError(
                f"Evaluator response missing score keys: {missing_keys}. "
                f"Full response: {text[:500]}"
            )

        return result
```

---

## 7. Server Entry Point

`openenv/app.py`

```python
"""
FastAPI server for the Slide Skill OpenEnv environment.

Endpoints follow the OpenEnv HTTP protocol:
    POST /reset                    → initialize or restart a session
    POST /step                     → apply an action and return observation
    DELETE /sessions/{session_id}  → clean up a session

The server is stateful: environment instances are kept in memory.
For production deployments with multiple workers, use a single-worker
Uvicorn setup or externalize session state to Redis.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from fastapi import Body, FastAPI, HTTPException, Path
from pydantic import BaseModel

from models import SlideSkillAction, SlideSkillObservation
from slide_skill_environment import SlideSkillEnvironment


# Single shared environment instance. Sessions are isolated at the file
# level, so this is safe for concurrent requests.
_env: SlideSkillEnvironment | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _env
    _env = SlideSkillEnvironment()
    yield
    _env = None


app = FastAPI(
    title="Slide Skill OpenEnv",
    description=(
        "OpenEnv-compatible environment for optimizing McKinsey-style "
        "PowerPoint slides by evolving DESIGN_RULES.md and EXAMPLES.md."
    ),
    lifespan=lifespan,
)


class ResetRequest(BaseModel):
    session_id: str | None = None


class ResetResponse(BaseModel):
    session_id: str
    message: str


class StepRequest(BaseModel):
    session_id: str
    action: SlideSkillAction


@app.post("/reset", response_model=ResetResponse)
async def reset(request: ResetRequest = Body(default=ResetRequest())) -> ResetResponse:
    """Initialize or restart an optimization session."""
    assert _env is not None
    session_id = _env.reset(session_id=request.session_id)
    return ResetResponse(
        session_id=session_id,
        message=f"Session {session_id} initialized with baseline skill files.",
    )


@app.post("/step", response_model=SlideSkillObservation)
async def step(request: StepRequest) -> SlideSkillObservation:
    """Apply an action to the session and return the resulting observation."""
    assert _env is not None
    try:
        observation = _env.step(
            session_id=request.session_id,
            action=request.action,
        )
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Session {request.session_id!r} not found. Call /reset first.",
        )
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return observation


@app.delete("/sessions/{session_id}")
async def close_session(
    session_id: Annotated[str, Path(description="Session ID to clean up.")]
) -> dict:
    """Clean up session resources (deletes /tmp/ working directory)."""
    assert _env is not None
    try:
        _env.close(session_id)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Session {session_id!r} not found.",
        )
    return {"message": f"Session {session_id} closed."}


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "supports_concurrent_sessions": True}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, workers=1)
```

---

## 8. Client

`openenv/client.py`

```python
"""
Reference client for the Slide Skill OpenEnv server.

Demonstrates how an optimizer agent would interact with the environment:
    1. Reset to get a session ID.
    2. Read the initial skill file contents from the first observation.
    3. Call an LLM optimizer to generate an improved DESIGN_RULES.md.
    4. Submit as a ReplaceFileAction.
    5. Repeat until done=True.

This client is also useful for smoke-testing the server without a full agent.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import Any

import anthropic
import httpx

from models import SlideSkillObservation

SERVER_URL = "http://localhost:8000"
OPTIMIZER_MODEL = "claude-opus-4-6"


class SlideSkillClient:
    """HTTP client for the Slide Skill OpenEnv server."""

    def __init__(self, base_url: str = SERVER_URL) -> None:
        self.base_url = base_url.rstrip("/")
        self._http = httpx.Client(timeout=300.0)  # long timeout for pipeline stages

    def reset(self, session_id: str | None = None) -> str:
        """Start a new session. Returns the session_id."""
        payload: dict[str, Any] = {}
        if session_id:
            payload["session_id"] = session_id
        resp = self._http.post(f"{self.base_url}/reset", json=payload)
        resp.raise_for_status()
        return resp.json()["session_id"]

    def step(self, session_id: str, action: dict) -> SlideSkillObservation:
        """
        Apply an action and return the observation.

        Args:
            session_id: Active session ID.
            action: Dict matching EditSectionAction or ReplaceFileAction schema.
                    Must include "action_type" key.
        """
        payload = {"session_id": session_id, "action": action}
        resp = self._http.post(f"{self.base_url}/step", json=payload)
        resp.raise_for_status()
        return SlideSkillObservation.model_validate(resp.json())

    def close(self, session_id: str) -> None:
        """Clean up the session."""
        resp = self._http.delete(f"{self.base_url}/sessions/{session_id}")
        resp.raise_for_status()

    def __enter__(self) -> SlideSkillClient:
        return self

    def __exit__(self, *_: Any) -> None:
        self._http.close()


# ---------------------------------------------------------------------------
# Optimizer agent (reference implementation)
# ---------------------------------------------------------------------------

def call_optimizer_llm(
    obs: SlideSkillObservation,
    anthropic_client: anthropic.Anthropic,
) -> dict:
    """
    Call the optimizer LLM to generate a new DESIGN_RULES.md based on
    the evaluation feedback.

    Returns a dict suitable for the step() action parameter.
    This uses ReplaceFileAction since the historical optimizer rewrites
    the file wholesale.
    """
    prompt = textwrap.dedent(f"""\
        You are a McKinsey slide design optimizer. You are improving a
        PowerPoint generation skill by rewriting its DESIGN_RULES.md file.

        ## Current Score: {obs.total}/100

        ## Score Breakdown
        - background_layout: {obs.scores.background_layout}/15
        - color_palette: {obs.scores.color_palette}/15
        - typography: {obs.scores.typography}/15
        - title_quality: {obs.scores.title_quality}/15
        - data_presentation: {obs.scores.data_presentation}/15
        - structural_elements: {obs.scores.structural_elements}/15
        - overall_impression: {obs.scores.overall_impression}/10

        ## Evaluator Feedback
        Strengths:
        {chr(10).join(f'- {s}' for s in obs.strengths)}

        Weaknesses:
        {chr(10).join(f'- {w}' for w in obs.weaknesses)}

        Verdict: {obs.one_line_verdict}

        ## Current DESIGN_RULES.md
        {obs.design_rules_content}

        ## Current EXAMPLES.md
        {obs.examples_content}

        Your task:
        Write an improved DESIGN_RULES.md that addresses the weaknesses above
        while preserving what works well. Focus on the dimensions with the
        lowest scores. Output ONLY the markdown file content — no explanation,
        no code fences.
    """)

    response = anthropic_client.messages.create(
        model=OPTIMIZER_MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    new_content = response.content[0].text.strip()

    return {
        "action_type": "replace_file",
        "file": "DESIGN_RULES.md",
        "new_content": new_content,
    }


def run_optimization_loop(server_url: str = SERVER_URL, max_steps: int = 7) -> None:
    """
    Run a full optimization episode using the LLM optimizer.

    This mirrors the historical Skill Forge loop but driven through the
    OpenEnv HTTP interface.
    """
    anthropic_client = anthropic.Anthropic()

    with SlideSkillClient(base_url=server_url) as client:
        session_id = client.reset()
        print(f"Session: {session_id}")

        # The first step must use the baseline skill files, so we submit a
        # no-op edit (replace EXAMPLES.md with its current content, which
        # forces the generator to run with the baseline DESIGN_RULES.md).
        # Alternatively, the server could expose a generate-only endpoint.
        print("Step 0: Generating baseline slide...")
        obs = client.step(
            session_id,
            {
                "action_type": "replace_file",
                "file": "EXAMPLES.md",
                "new_content": obs_initial_examples(client, session_id) if False else "(Empty — no prior optimization rounds)\n",
            },
        )
        print(f"  Baseline score: {obs.total}/100 — {obs.one_line_verdict}")

        for step_idx in range(1, max_steps + 1):
            if obs.done:
                print("Episode complete.")
                break

            print(f"\nStep {step_idx}: Calling optimizer LLM...")
            action = call_optimizer_llm(obs, anthropic_client)
            obs = client.step(session_id, action)

            print(
                f"  Score: {obs.total}/100 (reward: {obs.reward:+.3f}) "
                f"— {obs.one_line_verdict}"
            )
            print(f"  Weaknesses: {'; '.join(obs.weaknesses[:2])}")

        client.close(session_id)
        print(f"\nFinal score: {obs.total}/100")


if __name__ == "__main__":
    run_optimization_loop()
```

---

## 9. OpenEnv Manifest

`openenv/openenv.yaml`

```yaml
# OpenEnv environment manifest for Slide Skill
# https://openenv.dev/spec

name: slide-skill
version: "1.0.0"
description: >
  Self-improving McKinsey-style PowerPoint slide generation environment.
  The agent evolves DESIGN_RULES.md and EXAMPLES.md to maximize a visual
  design score (0-100) evaluated by Claude Opus vision against 5 McKinsey
  reference images.

author: Tesserae / Skill Forge Hackathon Team

supports_concurrent_sessions: true
max_steps: 7

# Approximate time budget per step (seconds).
# Each step: generator LLM (~20-40s) + Node.js (<5s) + LibreOffice (~15-30s)
# + pdftoppm (<5s) + evaluator LLM (~30-60s)
step_timeout_seconds: 180

action_space:
  type: union
  discriminator: action_type
  variants:
    - name: edit_section
      description: Replace the body of a named section in a skill file.
      fields:
        file: {type: string, enum: ["DESIGN_RULES.md", "EXAMPLES.md"]}
        section_heading: {type: string, description: "Exact heading text without # markers"}
        new_body: {type: string, description: "New section body content in markdown"}

    - name: replace_file
      description: Replace the entire content of a skill file.
      fields:
        file: {type: string, enum: ["DESIGN_RULES.md", "EXAMPLES.md"]}
        new_content: {type: string, description: "Complete new file content"}

observation_space:
  scores:
    background_layout: {type: integer, min: 0, max: 15}
    color_palette: {type: integer, min: 0, max: 15}
    typography: {type: integer, min: 0, max: 15}
    title_quality: {type: integer, min: 0, max: 15}
    data_presentation: {type: integer, min: 0, max: 15}
    structural_elements: {type: integer, min: 0, max: 15}
    overall_impression: {type: integer, min: 0, max: 10}
  total: {type: integer, min: 0, max: 100}
  strengths: {type: array, items: string}
  weaknesses: {type: array, items: string}
  one_line_verdict: {type: string}
  reward: {type: float, min: -0.3, max: 0.3}
  step: {type: integer}
  done: {type: boolean}
  jpg_path: {type: string, description: "Absolute path to generated slide JPG"}
  design_rules_content: {type: string}
  examples_content: {type: string}

reward:
  description: >
    Normalized score delta vs. previous step, capped to [-0.3, +0.3].
    Formula: clip(total_score - prev_total_score, -30, +30) / 100
  range: [-0.3, 0.3]

baseline:
  description: >
    skill_files_baseline/ committed to the repo contains the minimal
    starting DESIGN_RULES.md (teal palette, basic typography) and an
    empty EXAMPLES.md. This is skill_v0 content — NOT any evolved version.

endpoints:
  reset: POST /reset
  step: POST /step
  close: DELETE /sessions/{session_id}
  health: GET /health

server:
  host: 0.0.0.0
  port: 8000
  workers: 1  # Do not increase; LibreOffice is not thread-safe

environment_variables:
  required:
    - name: ANTHROPIC_API_KEY
      description: Anthropic API key for Claude generator and evaluator
  optional:
    - name: SLIDE_SKILL_MAX_STEPS
      description: Override default max_steps (default 7)
      default: "7"
```

---

## 10. Dockerfile

`openenv/Dockerfile`

```dockerfile
# Slide Skill OpenEnv — Docker image
#
# Layer sizes (approximate):
#   python:3.12-slim base:     ~130 MB
#   Node.js 20 + pptxgenjs:   ~200 MB
#   LibreOffice:               ~500 MB  <-- dominant cost
#   poppler-utils (pdftoppm):  ~30 MB
#   Python deps:               ~80 MB
# Total compressed: ~600-700 MB
#
# LibreOffice is the unavoidable bottleneck. It is required to convert
# .pptx → .pdf. There is no lighter alternative that handles pptxgenjs
# output faithfully.

FROM python:3.12-slim

LABEL description="Slide Skill OpenEnv — McKinsey PPT generation environment"

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # LibreOffice for .pptx → .pdf conversion
    libreoffice \
    # poppler-utils provides pdftoppm (.pdf → .jpg)
    poppler-utils \
    # Node.js 20 LTS via NodeSource
    curl \
    ca-certificates \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Verify tools are available
RUN node --version && npm --version && soffice --version && pdftoppm -v 2>&1 | head -1

WORKDIR /app

# Install pptxgenjs (Node.js dependency)
COPY package.json ./
RUN npm install --production

# Install Python dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e ".[server]"

# Copy application code
COPY pptx/ ./pptx/
COPY skill_files_baseline/ ./skill_files_baseline/
COPY output/TASK_PROMPT.md ./output/TASK_PROMPT.md
COPY output/reference/ ./output/reference/
COPY openenv/ ./openenv/

WORKDIR /app/openenv

# LibreOffice needs a writable user profile directory.
# Using /tmp/libreoffice-profile prevents concurrent session conflicts.
ENV HOME=/tmp
ENV SAL_USE_VCLPLUGIN=svp

EXPOSE 8000

# Single worker — LibreOffice is not thread-safe within one process.
# Concurrent sessions are handled by per-session /tmp/ directories,
# but LibreOffice calls must be serialized (or use process-level locking
# if scaling to multiple Gunicorn workers is required in the future).
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
```

---

## 11. Implementation Task Order

### Phase 1 — Foundation (no external dependencies)
1. Commit `skill_files_baseline/` to repo (copy `output/skill_v0/` content, verify EXAMPLES.md is truly minimal).
2. Implement `models.py` — pure Pydantic, no I/O.
3. Implement `skill_manager.py` — file I/O only, no LLM calls. Write unit tests with a tmp directory.
4. Implement `evaluator_adapter.py` — port the `evaluate_slide()` function from `output/evaluator.py`. Test against a known slide JPG and verify JSON matches expected structure.

### Phase 2 — Pipeline Integration
5. Implement `slide_generator.py` — integrate LLM call + subprocess chain. Test the four subprocess stages independently before wiring together.
6. Implement `slide_skill_environment.py` — wire `SkillManager` + `SlideGenerator` + `EvaluatorAdapter`. Test `reset()` creates isolated `/tmp/` dirs and `close()` removes them.

### Phase 3 — Server & Client
7. Implement `app.py` — FastAPI wrapper. Test `/health`, `/reset`, `/step` sequence with a minimal dummy action.
8. Implement `client.py` — test against the live server. Confirm the optimizer LLM loop produces an observation with improving scores.

### Phase 4 — Containerization
9. Write `Dockerfile`. Build and verify all four pipeline stages work inside the container.
10. Write `openenv.yaml`. Validate against the OpenEnv manifest schema.
11. Push to HuggingFace Spaces. Verify a full episode (7 steps) completes within resource limits.

### Phase 5 — Hardening
12. Add per-session LibreOffice locking if running >1 Uvicorn worker.
13. Add timeout handling in `_run()` and surface timeouts as proper HTTP 504 responses.
14. Add structured logging (JSON lines) so HuggingFace Spaces logs are parseable.

**Critical dependency note**: Phase 2 cannot start until Phase 1 is complete. Phase 3 cannot start until Phase 2 is stable. Phase 5 is optional for a hackathon demo but recommended for production.

---

## 12. Design Decisions and Rationale

### Per-Session Isolation vs. No-Concurrency

The original plan set `SUPPORTS_CONCURRENT_SESSIONS = False`. This is safe but prevents any parallel evaluation runs, making HuggingFace Spaces single-threaded even though the hardware could handle more.

The better approach is per-session file isolation: on `reset()`, copy both skill files into `/tmp/slide_skill_{session_id}/`. Each session's `generate.js`, `.pptx`, `.pdf`, and `.jpg` are written there too. Sessions never touch each other's files.

The one caveat is LibreOffice: `soffice` is not thread-safe when called concurrently from the same OS user. Options: (a) serialize LibreOffice calls with an `asyncio.Lock`, or (b) each session can set `--env HOME=/tmp/soffice_{session_id}` to get a unique LibreOffice user profile. Option (b) is simpler and is what the Dockerfile's `ENV HOME=/tmp` partially enables.

### Dual Action Types

The historical optimizer LLM rewrites the entire `DESIGN_RULES.md` in each round — it does not do surgical section edits. `ReplaceFileAction` matches this behavior exactly and makes the action space natural for an LLM optimizer.

`EditSectionAction` is retained because: (a) it is more token-efficient for small targeted changes, (b) it enables gradient-like optimization where an RL agent changes one dimension at a time, and (c) it is a cleaner action space for non-LLM optimizers (e.g., evolutionary algorithms).

Using a Pydantic discriminated union keeps the API clean: a single `action` field, type-safe dispatch in `SkillManager.apply()`, and automatic OpenAPI schema generation.

### Why We Don't Evolve the Generic pptx Skill

The files in `pptx/` (SKILL.md, editing.md, pptxgenjs.md) are the agent's API reference for using pptxgenjs. They are analogous to a standard library — stable, general-purpose, and not brand-specific. Evolving them would be like optimizing stdlib for one application.

The brand-specific optimization target is `DESIGN_RULES.md` + `EXAMPLES.md`. These encode McKinsey visual grammar: what colors, what typography, where to put structural elements, what titles should say. This separation is what makes the loop generalizable: swap in a different task prompt + reference images + baseline skill files, and the same environment can optimize slides for any brand.

### LibreOffice as the Bottleneck

LibreOffice adds ~500 MB to the Docker image and ~15–30 seconds per step. There is no lighter alternative that faithfully renders pptxgenjs output to PDF. Headless Chrome can render HTML but not .pptx. The pptxgenjs team does not offer a built-in PDF export.

Accept LibreOffice as a hard dependency. Optimize around it by: (a) keeping the Docker layer cached (don't change its installation order), (b) pre-warming LibreOffice on server startup with a dummy convert, (c) setting a 60-second timeout on the LibreOffice subprocess and surfacing timeout as a step error rather than hanging.

### Reward = Score Delta Capped at [-0.3, +0.3]

The evaluator is an LLM (Claude Opus 4.6 with vision). LLM evaluators have shot noise: the same slide evaluated twice may score 87 one time and 91 the next. If we use raw score delta as reward, a noise swing of +4 looks like a significant improvement. Capping at ±30 points (±0.3 normalized) means noise within ±5 points produces a small reward signal rather than a large one. The cap is soft for genuine improvements: going from 60→90 in one step (unusual but possible) gives reward = +0.3, same as going from 60→100. This is intentional — we want to reward improvement, not its magnitude, to keep the learning signal stable.

### EXAMPLES.md Grows Over Time

In the historical loop, `EXAMPLES.md` accumulated guidance across rounds — by v4, it referenced v3 and v4 issues explicitly. On `reset()`, we restore to the true `skill_v0` baseline: empty EXAMPLES.md. This is intentional. The optimizer must re-learn from the evaluator feedback each episode, which is the right behavior for RL. If you want warm-started episodes, implement a separate "curriculum baseline" and pass it as an optional `reset(skill_version="v3")` parameter.

---

## 13. Dependencies

`pyproject.toml`

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "slide-skill-openenv"
version = "1.0.0"
description = "OpenEnv environment for McKinsey-style PowerPoint slide optimization"
requires-python = ">=3.12"

# Core runtime dependencies (required for the environment to run)
dependencies = [
    "anthropic>=0.40.0",      # Claude API client (generator + evaluator)
    "pydantic>=2.6.0",        # Data models with discriminated unions
    "httpx>=0.27.0",          # HTTP client for client.py
]

[project.optional-dependencies]
# Server dependencies (required for app.py)
server = [
    "fastapi>=0.111.0",
    "uvicorn[standard]>=0.30.0",
    "python-multipart>=0.0.9",  # FastAPI form parsing
]

# Development and testing
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "httpx>=0.27.0",            # for FastAPI TestClient
    "ruff>=0.4.0",
    "mypy>=1.10.0",
]

[tool.hatch.build.targets.wheel]
packages = ["openenv"]

[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]

[tool.mypy]
python_version = "3.12"
strict = true
ignore_missing_imports = true
```
