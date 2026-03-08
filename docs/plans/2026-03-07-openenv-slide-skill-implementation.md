# OpenEnv Slide Skill Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build an OpenEnv environment that automatically optimizes PPT generation skills using three LLM roles: Opus optimizer, Sonnet executor, Gemini evaluator.

**Architecture:** Single `SlideSkillEnvironment` class with fat `step()` that internally runs optimize→generate→convert→evaluate. Internal logic split into separate modules. Uses OpenEnv's `Environment` base class with `Action`/`Observation`/`State` from `openenv.core.env_server.types`.

**Tech Stack:** openenv-core, anthropic SDK (0.84+), google-genai, FastAPI, pydantic, LibreOffice, poppler

---

### Task 1: Project Setup — pyproject.toml, requirements, .env.example

**Files:**
- Create: `pyproject.toml`
- Create: `openenv/requirements.txt`
- Create: `.env.example`
- Create: `skill_files_baseline/DESIGN_RULES.md`
- Create: `skill_files_baseline/EXAMPLES.md`

**Step 1: Create pyproject.toml**

```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "slide-skill-env"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "openenv-core",
    "anthropic>=0.84.0",
    "google-genai",
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
    "pydantic>=2.0",
    "python-dotenv",
]
```

**Step 2: Create openenv/requirements.txt**

```
openenv-core
anthropic>=0.84.0
google-genai
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.0
python-dotenv
```

**Step 3: Create .env.example**

```
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
SLIDE_SKILL_MAX_STEPS=7
SLIDE_SKILL_SCORE_THRESHOLD=90
SLIDE_SKILL_PLATEAU_PATIENCE=2
```

**Step 4: Copy baseline skill files**

Copy `output/skill_v0/DESIGN_RULES.md` to `skill_files_baseline/DESIGN_RULES.md`.
Create `skill_files_baseline/EXAMPLES.md` with content:
```markdown
# Examples
(Empty — no prior optimization rounds)
```

**Step 5: Install dependencies**

Run: `pip install -e .`
Expected: installs successfully

**Step 6: Commit**

```bash
git add pyproject.toml openenv/requirements.txt .env.example skill_files_baseline/
git commit -m "chore: add project setup, dependencies, and baseline skill files"
```

---

### Task 2: Data Models — models.py

**Files:**
- Create: `openenv/__init__.py`
- Create: `openenv/models.py`

**Step 1: Create openenv/__init__.py**

Empty file.

**Step 2: Create openenv/models.py**

```python
"""Pydantic models for the Slide Skill OpenEnv environment."""

from typing import Any

from pydantic import Field

from openenv.core.env_server.types import Action, Observation, State


class SkillAction(Action):
    """Action sent by the client each step."""

    hint: str | None = Field(
        default=None,
        description="Optional guidance for the optimizer, e.g. 'focus on typography'",
    )


class SkillObservation(Observation):
    """Observation returned after each step."""

    step_number: int = Field(description="Current step number in the episode")
    scores: dict[str, int] = Field(
        description="Scores per dimension, e.g. {'background_layout': 14, ...}"
    )
    total: int = Field(description="Sum of all scores, 0-100")
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    one_line_verdict: str = Field(default="")
    skill_files: dict[str, str] = Field(
        description="Current skill folder contents: filename -> content"
    )
    slide_image_base64: str = Field(
        default="", description="Rendered slide as base64 JPEG"
    )
    done_reason: str | None = Field(
        default=None, description="Why the episode ended: threshold, plateau, max_steps"
    )


class SkillState(State):
    """Internal episode state."""

    score_history: list[int] = Field(default_factory=list)
    best_score: int = Field(default=0)
    best_skill_files: dict[str, str] = Field(default_factory=dict)
    max_steps: int = Field(default=7)
    score_threshold: int = Field(default=90)
    plateau_patience: int = Field(default=2)
```

**Step 3: Verify models import correctly**

Run: `python -c "from openenv.models import SkillAction, SkillObservation, SkillState; print('OK')"`
Expected: `OK`

**Step 4: Commit**

```bash
git add openenv/
git commit -m "feat: add data models for SkillAction, SkillObservation, SkillState"
```

---

### Task 3: Skill Manager — skill_manager.py

**Files:**
- Create: `openenv/skill_manager.py`

**Step 1: Create skill_manager.py**

```python
"""Manages the skill folder — read, write, list, delete, copy baseline."""

import shutil
from pathlib import Path

BASELINE_DIR = Path(__file__).parent.parent / "skill_files_baseline"


class SkillManager:
    """File operations on a skill folder within an episode's temp directory."""

    def __init__(self, skill_dir: Path):
        self.skill_dir = skill_dir

    def init_from_baseline(self) -> None:
        """Copy baseline skill files into the working directory."""
        self.skill_dir.mkdir(parents=True, exist_ok=True)
        for f in BASELINE_DIR.iterdir():
            if f.is_file():
                shutil.copy2(f, self.skill_dir / f.name)

    def read_file(self, filename: str) -> str:
        path = self.skill_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Skill file not found: {filename}")
        return path.read_text()

    def write_file(self, filename: str, content: str) -> None:
        path = self.skill_dir / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def delete_file(self, filename: str) -> None:
        path = self.skill_dir / filename
        if path.exists():
            path.unlink()

    def list_files(self) -> list[str]:
        if not self.skill_dir.exists():
            return []
        return [f.name for f in self.skill_dir.iterdir() if f.is_file()]

    def read_all(self) -> dict[str, str]:
        """Return all skill files as {filename: content}."""
        return {name: self.read_file(name) for name in self.list_files()}

    def snapshot(self) -> dict[str, str]:
        """Return a frozen copy of all skill files."""
        return dict(self.read_all())
```

**Step 2: Verify**

Run: `python -c "from openenv.skill_manager import SkillManager; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add openenv/skill_manager.py
git commit -m "feat: add SkillManager for skill folder file operations"
```

---

### Task 4: Converter — converter.py

**Files:**
- Create: `openenv/converter.py`

**Step 1: Create converter.py**

```python
"""Convert .pptx → .pdf → .jpg using LibreOffice and poppler."""

import subprocess
from pathlib import Path


def pptx_to_jpg(pptx_path: Path, output_dir: Path) -> Path:
    """Convert a .pptx file to a JPEG image of the first slide.

    Args:
        pptx_path: Path to the .pptx file.
        output_dir: Directory to write intermediate and final files.

    Returns:
        Path to the rendered JPEG image.

    Raises:
        RuntimeError: If conversion fails at any step.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / pptx_path.with_suffix(".pdf").name

    # Step 1: pptx → pdf via LibreOffice
    result = subprocess.run(
        [
            "soffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", str(output_dir),
            str(pptx_path),
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0 or not pdf_path.exists():
        raise RuntimeError(
            f"LibreOffice conversion failed: {result.stderr}"
        )

    # Step 2: pdf → jpg via pdftoppm (first page only)
    jpg_prefix = output_dir / "slide"
    result = subprocess.run(
        [
            "pdftoppm",
            "-jpeg", "-r", "150",
            "-f", "1", "-l", "1",
            str(pdf_path),
            str(jpg_prefix),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(f"pdftoppm conversion failed: {result.stderr}")

    # pdftoppm outputs slide-1.jpg or slide-01.jpg
    candidates = list(output_dir.glob("slide-*.jpg"))
    if not candidates:
        raise RuntimeError("No JPEG output found from pdftoppm")
    return candidates[0]
```

**Step 2: Verify import**

Run: `python -c "from openenv.converter import pptx_to_jpg; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add openenv/converter.py
git commit -m "feat: add pptx-to-jpg converter using LibreOffice and poppler"
```

---

### Task 5: Evaluator — evaluator.py

**Files:**
- Create: `openenv/evaluator.py`

**Step 1: Create evaluator.py**

This adapts the existing `output/evaluator.py` rubric to use Gemini 3.1 Pro Preview instead of Claude, and accepts reference images as arguments rather than hardcoding paths.

```python
"""Evaluate slide images against references using Gemini 3.1 Pro Preview."""

import base64
import json
import os
from pathlib import Path

from google import genai
from google.genai import types

EVALUATION_RUBRIC = """You are an expert slide design evaluator.

You will be shown:
1. REFERENCE IMAGES: Gold-standard slides provided by the user. These represent the target visual style.
2. CANDIDATE SLIDE: A programmatically generated slide rendered as a JPEG image.

Score how closely the CANDIDATE SLIDE matches the visual style in the REFERENCE IMAGES.

## Scoring Rubric (100 points total)

### 1. Background & Base Layout (0-15 points)
- Clean background matching reference style
- Proper margins (~0.5" all sides)
- No unnecessary visual clutter

### 2. Color Palette Fidelity (0-15 points)
- Matches reference color palette
- Restrained, professional palette
- Accent colors used sparingly

### 3. Typography (0-15 points)
- Font hierarchy matches reference
- Clear size hierarchy: title >> subtitle >> body >> footnotes

### 4. Title Quality — "So-What" Style (0-15 points)
- Insight-driven conclusion title, not just a topic label
- Title tells the key takeaway without reading the slide

### 5. Data Presentation (0-15 points)
- Data format matches reference style (tables, charts, etc.)
- Organized, scannable, well-structured

### 6. Structural Elements (0-15 points)
- Divider lines, footers, footnotes matching reference
- Source attribution, page numbers present

### 7. Overall Visual Impression (0-10 points)
- Does this feel like it came from the same source as the references?
- Clean, restrained, and authoritative

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


def evaluate_slide(
    slide_image: bytes,
    reference_images: list[bytes],
    api_key: str | None = None,
) -> dict:
    """Score a slide image against reference images using Gemini vision.

    Args:
        slide_image: JPEG bytes of the candidate slide.
        reference_images: List of JPEG bytes for reference slides.
        api_key: Gemini API key (falls back to GEMINI_API_KEY env var).

    Returns:
        Dict with scores, total, strengths, weaknesses, one_line_verdict.
    """
    key = api_key or os.environ["GEMINI_API_KEY"]
    client = genai.Client(api_key=key)

    # Build content parts
    parts = []
    parts.append(types.Part.from_text(
        "## REFERENCE IMAGES (Gold standard)\n"
        "Study these reference slides carefully. The candidate should match this style."
    ))
    for i, ref_bytes in enumerate(reference_images):
        parts.append(types.Part.from_bytes(data=ref_bytes, mime_type="image/jpeg"))
        parts.append(types.Part.from_text(f"(Reference {i + 1})"))

    parts.append(types.Part.from_text(
        "\n## CANDIDATE SLIDE TO EVALUATE"
    ))
    parts.append(types.Part.from_bytes(data=slide_image, mime_type="image/jpeg"))
    parts.append(types.Part.from_text(
        "\nScore this candidate against the references using the rubric. "
        "Return ONLY the JSON object."
    ))

    response = client.models.generate_content(
        model="gemini-3.1-pro-preview",
        contents=[types.Content(role="user", parts=parts)],
        config=types.GenerateContentConfig(
            system_instruction=EVALUATION_RUBRIC,
            temperature=0.2,
            max_output_tokens=1024,
        ),
    )

    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text)
```

**Step 2: Verify import**

Run: `python -c "from openenv.evaluator import evaluate_slide; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add openenv/evaluator.py
git commit -m "feat: add Gemini 3.1 Pro Preview slide evaluator"
```

---

### Task 6: Generator — generator.py

**Files:**
- Create: `openenv/generator.py`

**Step 1: Create generator.py**

Uses Claude Sonnet 4.6 with the managed pptx skill and code execution to generate slides. Downloads the resulting .pptx via the Files API.

```python
"""Generate slides using Claude Sonnet 4.6 + managed pptx skill."""

import os
from pathlib import Path

import anthropic


def generate_slide(
    task_prompt: str,
    skill_files: dict[str, str],
    output_path: Path,
    api_key: str | None = None,
) -> Path:
    """Generate a .pptx slide using Claude Sonnet with the pptx skill.

    Args:
        task_prompt: What slide to generate.
        skill_files: Skill folder contents {filename: content}.
        output_path: Where to save the downloaded .pptx file.
        api_key: Anthropic API key (falls back to ANTHROPIC_API_KEY env var).

    Returns:
        Path to the saved .pptx file.

    Raises:
        RuntimeError: If generation or download fails.
    """
    key = api_key or os.environ["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=key)

    # Build message with skill files as context
    skill_context = ""
    for filename, content in skill_files.items():
        skill_context += f"\n### {filename}\n```\n{content}\n```\n"

    message_content = (
        f"Follow these design rules exactly when generating the slide:\n"
        f"{skill_context}\n\n"
        f"## Task\n{task_prompt}"
    )

    response = client.beta.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=16384,
        betas=["code-execution-2025-08-25", "skills-2025-10-02"],
        container={
            "skills": [
                {"type": "anthropic", "skill_id": "pptx", "version": "latest"}
            ]
        },
        messages=[{"role": "user", "content": message_content}],
        tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    )

    # Extract file_id from response
    file_id = _extract_file_id(response)
    if not file_id:
        raise RuntimeError(
            "No file was generated. Response: "
            + str([b.type for b in response.content])
        )

    # Download the file
    file_content = client.beta.files.download(
        file_id=file_id, betas=["files-api-2025-04-14"]
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        file_content.write_to_file(f.name)

    return output_path


def _extract_file_id(response) -> str | None:
    """Extract file_id from a code execution response."""
    for block in response.content:
        if block.type == "tool_result":
            for item in block.content:
                if hasattr(item, "file_id"):
                    return item.file_id
        # Also check for server-tool-use results
        if block.type == "server_tool_use":
            continue
        if block.type == "server_tool_result":
            for item in getattr(block, "content", []):
                if hasattr(item, "file_id"):
                    return item.file_id
    return None
```

**Step 2: Verify import**

Run: `python -c "from openenv.generator import generate_slide; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add openenv/generator.py
git commit -m "feat: add slide generator using Claude Sonnet 4.6 + pptx skill"
```

---

### Task 7: Optimizer — optimizer.py

**Files:**
- Create: `openenv/optimizer.py`

**Step 1: Create optimizer.py**

This is the agentic component — Claude Opus 4.6 with tool use in a multi-turn loop. It reads the evaluation feedback and edits skill files via tools.

```python
"""Agentic optimizer using Claude Opus 4.6 with file tools."""

import base64
import os

import anthropic

from openenv.skill_manager import SkillManager

OPTIMIZER_SYSTEM = """You are a slide design skill optimizer. You improve design rule files
so that slides generated from them better match the reference style.

You have tools to read, write, list, and delete files in the skill folder.
The skill folder contains markdown files (like DESIGN_RULES.md, EXAMPLES.md)
that guide a slide generator.

Based on the evaluation feedback and reference images, decide what changes
to make. You can:
- Edit existing files to fix issues identified in the feedback
- Add new files (e.g., COLOR_RULES.md, LAYOUT_PATTERNS.md) if the skill
  needs more structure
- Delete files that are counterproductive
- Add helper scripts if needed

Focus on the weaknesses identified by the evaluator. Make targeted changes
that address specific issues rather than rewriting everything."""

# Tool definitions for the optimizer agent
OPTIMIZER_TOOLS = [
    {
        "name": "read_file",
        "description": "Read the contents of a file in the skill folder.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Name of the file to read"}
            },
            "required": ["filename"],
        },
    },
    {
        "name": "write_file",
        "description": "Write content to a file in the skill folder. Creates or overwrites.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Name of the file to write"},
                "content": {"type": "string", "description": "Full file content to write"},
            },
            "required": ["filename", "content"],
        },
    },
    {
        "name": "delete_file",
        "description": "Delete a file from the skill folder.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Name of the file to delete"}
            },
            "required": ["filename"],
        },
    },
    {
        "name": "list_files",
        "description": "List all files currently in the skill folder.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
]


def optimize_skill(
    skill_manager: SkillManager,
    evaluation: dict,
    reference_images: list[bytes],
    hint: str | None = None,
    api_key: str | None = None,
) -> None:
    """Run the optimizer agent to improve skill files in-place.

    Args:
        skill_manager: SkillManager pointing to the working skill folder.
        evaluation: Previous evaluation results (scores, strengths, weaknesses).
        reference_images: User-provided reference images as bytes.
        hint: Optional guidance from the client.
        api_key: Anthropic API key.
    """
    key = api_key or os.environ["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=key)

    # Build the user message with feedback, current files, and references
    current_files = skill_manager.read_all()
    files_str = ""
    for name, content in current_files.items():
        files_str += f"\n### {name}\n```\n{content}\n```\n"

    # Build content parts (text + images)
    content_parts = []

    # Reference images
    content_parts.append({
        "type": "text",
        "text": "## Reference Images (target style)\nStudy these carefully:",
    })
    for i, img_bytes in enumerate(reference_images):
        content_parts.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": base64.standard_b64encode(img_bytes).decode(),
            },
        })

    # Evaluation feedback
    feedback_text = (
        f"\n## Previous Evaluation\n"
        f"Total score: {evaluation.get('total', 'N/A')}/100\n\n"
        f"**Strengths:**\n"
    )
    for s in evaluation.get("strengths", []):
        feedback_text += f"- {s}\n"
    feedback_text += f"\n**Weaknesses (FIX THESE):**\n"
    for w in evaluation.get("weaknesses", []):
        feedback_text += f"- {w}\n"
    feedback_text += f"\n**Verdict:** {evaluation.get('one_line_verdict', '')}\n"

    content_parts.append({"type": "text", "text": feedback_text})

    # Current skill files
    content_parts.append({
        "type": "text",
        "text": f"\n## Current Skill Files\n{files_str}",
    })

    # Hint
    if hint:
        content_parts.append({
            "type": "text",
            "text": f"\n## Additional Guidance\n{hint}",
        })

    content_parts.append({
        "type": "text",
        "text": (
            "\nUse your tools to improve the skill files. Focus on fixing "
            "the weaknesses. Start by listing current files, then make changes."
        ),
    })

    # Multi-turn tool use loop
    messages = [{"role": "user", "content": content_parts}]

    for _ in range(20):  # Safety limit on tool calls
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,
            system=OPTIMIZER_SYSTEM,
            messages=messages,
            tools=OPTIMIZER_TOOLS,
        )

        # Process response
        if response.stop_reason == "end_turn":
            break

        # Handle tool use
        assistant_content = response.content
        messages.append({"role": "assistant", "content": assistant_content})

        tool_results = []
        for block in assistant_content:
            if block.type == "tool_use":
                result = _execute_tool(skill_manager, block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

        if tool_results:
            messages.append({"role": "user", "content": tool_results})
        else:
            break


def _execute_tool(skill_manager: SkillManager, tool_name: str, tool_input: dict) -> str:
    """Execute a tool call and return the result as a string."""
    try:
        if tool_name == "read_file":
            return skill_manager.read_file(tool_input["filename"])
        elif tool_name == "write_file":
            skill_manager.write_file(tool_input["filename"], tool_input["content"])
            return f"Written: {tool_input['filename']}"
        elif tool_name == "delete_file":
            skill_manager.delete_file(tool_input["filename"])
            return f"Deleted: {tool_input['filename']}"
        elif tool_name == "list_files":
            files = skill_manager.list_files()
            return "\n".join(files) if files else "(empty)"
        else:
            return f"Unknown tool: {tool_name}"
    except Exception as e:
        return f"Error: {e}"
```

**Step 2: Verify import**

Run: `python -c "from openenv.optimizer import optimize_skill; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add openenv/optimizer.py
git commit -m "feat: add agentic optimizer using Claude Opus 4.6 with file tools"
```

---

### Task 8: Environment — slide_skill_environment.py

**Files:**
- Create: `openenv/slide_skill_environment.py`

**Step 1: Create slide_skill_environment.py**

```python
"""Main OpenEnv environment — orchestrates optimize → generate → evaluate."""

import base64
import shutil
import tempfile
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

from openenv.core.env_server.types import Environment

from openenv.converter import pptx_to_jpg
from openenv.evaluator import evaluate_slide
from openenv.generator import generate_slide
from openenv.models import SkillAction, SkillObservation, SkillState
from openenv.optimizer import optimize_skill
from openenv.skill_manager import SkillManager

import os
from dotenv import load_dotenv

load_dotenv()


class SlideSkillEnvironment(Environment[SkillAction, SkillObservation, SkillState]):
    """OpenEnv environment for self-improving PPT skill optimization."""

    def __init__(self):
        super().__init__()
        self._state = SkillState()
        self._episode_dir: Path | None = None
        self._skill_manager: SkillManager | None = None
        self._reference_images: list[bytes] = []
        self._task_prompt: str = ""
        self._last_evaluation: dict = {}

    def reset(
        self,
        seed: Optional[int] = None,
        episode_id: Optional[str] = None,
        **kwargs: Any,
    ) -> SkillObservation:
        """Start a new episode.

        Expected kwargs:
            reference_images: list[str]  # base64-encoded JPEG images
            task_prompt: str
            baseline_skill: dict[str, str] | None  # {filename: content}
            max_steps: int (default 7)
            score_threshold: int (default 90)
            plateau_patience: int (default 2)
        """
        # Cleanup previous episode
        self._cleanup()

        # Parse config
        eid = episode_id or str(uuid4())
        self._task_prompt = kwargs.get("task_prompt", "Generate a presentation slide")
        max_steps = int(kwargs.get("max_steps", os.getenv("SLIDE_SKILL_MAX_STEPS", 7)))
        score_threshold = int(kwargs.get(
            "score_threshold", os.getenv("SLIDE_SKILL_SCORE_THRESHOLD", 90)
        ))
        plateau_patience = int(kwargs.get(
            "plateau_patience", os.getenv("SLIDE_SKILL_PLATEAU_PATIENCE", 2)
        ))

        # Decode reference images
        raw_refs = kwargs.get("reference_images", [])
        self._reference_images = [
            base64.b64decode(img) if isinstance(img, str) else img
            for img in raw_refs
        ]

        # Setup temp directory
        self._episode_dir = Path(tempfile.mkdtemp(prefix=f"slide_skill_{eid}_"))
        skill_dir = self._episode_dir / "skill"
        slides_dir = self._episode_dir / "slides"
        slides_dir.mkdir()

        # Initialize skill folder
        self._skill_manager = SkillManager(skill_dir)
        baseline = kwargs.get("baseline_skill")
        if baseline and isinstance(baseline, dict):
            skill_dir.mkdir(parents=True, exist_ok=True)
            for name, content in baseline.items():
                self._skill_manager.write_file(name, content)
        else:
            self._skill_manager.init_from_baseline()

        # Initialize state
        self._state = SkillState(
            episode_id=eid,
            step_count=0,
            score_history=[],
            best_score=0,
            best_skill_files={},
            max_steps=max_steps,
            score_threshold=score_threshold,
            plateau_patience=plateau_patience,
        )

        # Run initial generate → evaluate to get baseline score
        skill_files = self._skill_manager.snapshot()
        pptx_path = slides_dir / "slide_step_0.pptx"
        generate_slide(self._task_prompt, skill_files, pptx_path)
        jpg_path = pptx_to_jpg(pptx_path, slides_dir)
        slide_bytes = jpg_path.read_bytes()

        evaluation = evaluate_slide(slide_bytes, self._reference_images)
        self._last_evaluation = evaluation
        total = evaluation.get("total", 0)
        self._state.score_history.append(total)
        self._state.best_score = total
        self._state.best_skill_files = skill_files

        return SkillObservation(
            step_number=0,
            scores=evaluation.get("scores", {}),
            total=total,
            reward=0.0,
            strengths=evaluation.get("strengths", []),
            weaknesses=evaluation.get("weaknesses", []),
            one_line_verdict=evaluation.get("one_line_verdict", ""),
            skill_files=skill_files,
            slide_image_base64=base64.b64encode(slide_bytes).decode(),
            done=False,
            done_reason=None,
        )

    def step(
        self,
        action: SkillAction,
        timeout_s: Optional[float] = None,
        **kwargs: Any,
    ) -> SkillObservation:
        """Run one optimize → generate → convert → evaluate cycle."""
        self._state.step_count += 1
        step_num = self._state.step_count
        slides_dir = self._episode_dir / "slides"

        # 1. OPTIMIZE
        optimize_skill(
            skill_manager=self._skill_manager,
            evaluation=self._last_evaluation,
            reference_images=self._reference_images,
            hint=action.hint if isinstance(action, SkillAction) else None,
        )

        # 2. GENERATE
        skill_files = self._skill_manager.snapshot()
        pptx_path = slides_dir / f"slide_step_{step_num}.pptx"
        generate_slide(self._task_prompt, skill_files, pptx_path)

        # 3. CONVERT
        jpg_path = pptx_to_jpg(pptx_path, slides_dir)
        slide_bytes = jpg_path.read_bytes()

        # 4. EVALUATE
        evaluation = evaluate_slide(slide_bytes, self._reference_images)
        self._last_evaluation = evaluation
        total = evaluation.get("total", 0)

        # Update state
        prev_score = self._state.score_history[-1] if self._state.score_history else 0
        reward = (total - prev_score) / 100.0
        reward = max(-0.3, min(0.3, reward))  # Cap reward
        self._state.score_history.append(total)

        if total > self._state.best_score:
            self._state.best_score = total
            self._state.best_skill_files = skill_files

        # 5. CHECK DONE
        done, done_reason = self._check_done()

        return SkillObservation(
            step_number=step_num,
            scores=evaluation.get("scores", {}),
            total=total,
            reward=reward,
            strengths=evaluation.get("strengths", []),
            weaknesses=evaluation.get("weaknesses", []),
            one_line_verdict=evaluation.get("one_line_verdict", ""),
            skill_files=skill_files,
            slide_image_base64=base64.b64encode(slide_bytes).decode(),
            done=done,
            done_reason=done_reason,
        )

    def _check_done(self) -> tuple[bool, str | None]:
        """Check if the episode should end."""
        history = self._state.score_history
        step = self._state.step_count

        # Max steps
        if step >= self._state.max_steps:
            return True, "max_steps"

        # Score threshold
        if history and history[-1] >= self._state.score_threshold:
            return True, "threshold"

        # Plateau
        patience = self._state.plateau_patience
        if len(history) > patience:
            recent = history[-patience:]
            if all(s <= history[-patience - 1] for s in recent):
                return True, "plateau"

        return False, None

    @property
    def state(self) -> SkillState:
        return self._state

    def close(self) -> None:
        self._cleanup()

    def _cleanup(self) -> None:
        if self._episode_dir and self._episode_dir.exists():
            shutil.rmtree(self._episode_dir, ignore_errors=True)
        self._episode_dir = None
        self._skill_manager = None
```

**Step 2: Verify import**

Run: `python -c "from openenv.slide_skill_environment import SlideSkillEnvironment; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add openenv/slide_skill_environment.py
git commit -m "feat: add SlideSkillEnvironment with full optimize-generate-evaluate loop"
```

---

### Task 9: FastAPI App — app.py

**Files:**
- Create: `openenv/app.py`

**Step 1: Create app.py**

```python
"""FastAPI application for the Slide Skill environment."""

from openenv.core.env_server.http_server import create_app

from openenv.models import SkillAction, SkillObservation
from openenv.slide_skill_environment import SlideSkillEnvironment

app = create_app(
    SlideSkillEnvironment,
    SkillAction,
    SkillObservation,
    env_name="slide_skill",
)


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
```

**Step 2: Verify import**

Run: `python -c "from openenv.app import app; print(type(app))"`
Expected: `<class 'fastapi.applications.FastAPI'>`

**Step 3: Commit**

```bash
git add openenv/app.py
git commit -m "feat: add FastAPI app using OpenEnv create_app"
```

---

### Task 10: OpenEnv Manifest — openenv.yaml

**Files:**
- Create: `openenv/openenv.yaml`

**Step 1: Create openenv.yaml**

```yaml
name: slide-skill
version: "0.1.0"
description: >
  Self-improving PPT skill environment. Optimizes slide design rules
  through iterative generate-evaluate-optimize cycles using three LLM roles:
  Claude Opus (optimizer), Claude Sonnet (generator), Gemini (evaluator).
```

**Step 2: Commit**

```bash
git add openenv/openenv.yaml
git commit -m "chore: add OpenEnv manifest"
```

---

### Task 11: Dockerfile

**Files:**
- Create: `openenv/Dockerfile`

**Step 1: Create Dockerfile**

```dockerfile
FROM python:3.12-slim

# Node.js 20 for pptxgenjs
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# LibreOffice for pptx → pdf conversion
RUN apt-get update && \
    apt-get install -y --no-install-recommends libreoffice-impress && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Poppler for pdf → jpg conversion
RUN apt-get update && \
    apt-get install -y --no-install-recommends poppler-utils && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY openenv/requirements.txt openenv/requirements.txt
RUN pip install --no-cache-dir -r openenv/requirements.txt

# Copy project files
COPY package.json package-lock.json ./
RUN npm ci --production

COPY openenv/ openenv/
COPY skill_files_baseline/ skill_files_baseline/
COPY pptx/ pptx/

EXPOSE 8000
CMD ["uvicorn", "openenv.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
```

**Step 2: Commit**

```bash
git add openenv/Dockerfile
git commit -m "chore: add Dockerfile with Node.js, LibreOffice, and poppler"
```

---

### Task 12: Client Script — client.py

**Files:**
- Create: `openenv/client.py`

**Step 1: Create client.py**

A reference client that runs the full optimization loop against the server.

```python
"""Reference client for the Slide Skill environment."""

import argparse
import asyncio
import base64
import json
import sys
from pathlib import Path

import httpx


async def run_episode(
    server_url: str,
    reference_dir: Path,
    task_prompt: str,
    max_steps: int = 7,
    smoke_test: bool = False,
):
    """Run one optimization episode against the server."""
    # Load reference images
    ref_images = []
    for img_path in sorted(reference_dir.glob("*.jpg")):
        ref_images.append(base64.b64encode(img_path.read_bytes()).decode())
    if not ref_images:
        print(f"ERROR: No .jpg files found in {reference_dir}")
        sys.exit(1)
    print(f"Loaded {len(ref_images)} reference images from {reference_dir}")

    async with httpx.AsyncClient(timeout=300.0) as client:
        # Reset
        print("\n--- Reset ---")
        reset_resp = await client.post(
            f"{server_url}/reset",
            json={
                "reference_images": ref_images,
                "task_prompt": task_prompt,
                "max_steps": 1 if smoke_test else max_steps,
            },
        )
        reset_resp.raise_for_status()
        obs = reset_resp.json()["observation"]
        print(f"Baseline score: {obs['total']}/100")
        print(f"Verdict: {obs.get('one_line_verdict', '')}")

        if smoke_test:
            # Run one step and exit
            print("\n--- Smoke Test: 1 step ---")
            step_resp = await client.post(
                f"{server_url}/step",
                json={"action": {"hint": None}},
            )
            step_resp.raise_for_status()
            obs = step_resp.json()["observation"]
            print(f"Step 1 score: {obs['total']}/100")
            print(f"Verdict: {obs.get('one_line_verdict', '')}")
            print(f"Done: {obs['done']} (reason: {obs.get('done_reason')})")
            return

        # Optimization loop
        step = 0
        while not obs.get("done", False):
            step += 1
            print(f"\n--- Step {step} ---")
            step_resp = await client.post(
                f"{server_url}/step",
                json={"action": {"hint": None}},
            )
            step_resp.raise_for_status()
            obs = step_resp.json()["observation"]
            print(f"Score: {obs['total']}/100 (reward: {obs.get('reward', 0):+.3f})")
            print(f"Verdict: {obs.get('one_line_verdict', '')}")
            if obs.get("weaknesses"):
                print(f"Top weakness: {obs['weaknesses'][0]}")

        print(f"\n=== Episode Complete ===")
        print(f"Final score: {obs['total']}/100")
        print(f"Reason: {obs.get('done_reason')}")
        print(f"Skill files: {list(obs.get('skill_files', {}).keys())}")


def main():
    parser = argparse.ArgumentParser(description="Slide Skill OpenEnv Client")
    parser.add_argument(
        "--server", default="http://localhost:8000", help="Server URL"
    )
    parser.add_argument(
        "--references",
        default="output/reference",
        help="Directory with reference .jpg images",
    )
    parser.add_argument(
        "--task",
        default=(
            "Generate a 1-slide timeline PowerPoint about Dutch Hydrogen "
            "Strategy (2020-2035) in McKinsey consulting style."
        ),
        help="Task prompt",
    )
    parser.add_argument("--max-steps", type=int, default=7)
    parser.add_argument("--smoke-test", action="store_true")
    args = parser.parse_args()

    asyncio.run(
        run_episode(
            server_url=args.server,
            reference_dir=Path(args.references),
            task_prompt=args.task,
            max_steps=args.max_steps,
            smoke_test=args.smoke_test,
        )
    )


if __name__ == "__main__":
    main()
```

**Step 2: Verify import**

Run: `python -c "from openenv.client import run_episode; print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add openenv/client.py
git commit -m "feat: add reference client with optimization loop and smoke test"
```

---

### Task 13: Smoke Test — End-to-End Verification

**Step 1: Verify all imports work**

Run: `python -c "from openenv.app import app; from openenv.models import SkillAction, SkillObservation; from openenv.slide_skill_environment import SlideSkillEnvironment; print('All imports OK')"`
Expected: `All imports OK`

**Step 2: Verify .env is configured**

Run: `test -f .env && echo '.env exists' || echo 'Copy .env.example to .env and fill in API keys'`

**Step 3: Start server**

Run: `uvicorn openenv.app:app --host 0.0.0.0 --port 8000 &`
Expected: server starts on port 8000

**Step 4: Run smoke test**

Run: `python openenv/client.py --server http://localhost:8000 --smoke-test`
Expected: Baseline score printed, one step runs, score printed, done.

**Step 5: Kill server and commit**

```bash
kill %1
git add -A
git commit -m "chore: verify end-to-end smoke test passes"
```

---

### Task 14: Docker Build & Test

**Step 1: Build Docker image**

Run: `docker build -f openenv/Dockerfile -t slide-skill-openenv .`
Expected: builds successfully (~700-800MB)

**Step 2: Run container**

Run: `docker run -p 8000:8000 --env-file .env slide-skill-openenv`
Expected: server starts

**Step 3: Run smoke test against container**

Run (in separate terminal): `python openenv/client.py --server http://localhost:8000 --smoke-test`
Expected: Same as Task 13 Step 4

**Step 4: Commit any fixes**

```bash
git add -A
git commit -m "chore: verify Docker build and smoke test"
```
