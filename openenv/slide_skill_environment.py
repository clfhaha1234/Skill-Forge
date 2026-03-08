"""
Slide Skill Environment — OpenEnv-compatible environment for optimizing
McKinsey-style PowerPoint slide generation.

Concurrency model:
    SUPPORTS_CONCURRENT_SESSIONS = True

    Each session gets an isolated working directory at /tmp/slide_skill_{session_id}/.
    All skill files (DESIGN_RULES.md, EXAMPLES.md, SKILL.md, editing.md,
    pptxgenjs.md) are copied there on reset() and modified in place during
    the session. The shared repo files are never modified.

Episode timing:
    Each step involves two LLM calls (generator + evaluator) plus Node.js and
    LibreOffice. Expect 60-120 seconds per step. At max_steps=7, a full episode
    runs 7-14 minutes.

Reward function:
    reward = clip(total_score - prev_total_score, -30, +30) / 100
    Capping at +/-30 points (+/-0.3 reward) dampens LLM evaluation noise.
"""

from __future__ import annotations

import os
import shutil
import uuid
from pathlib import Path
from typing import ClassVar

from models import (
    SlideScores,
    SlideSkillAction,
    SlideSkillObservation,
    SlideSkillState,
)
from skill_manager import SkillManager
from slide_generator import SlideGenerator
from evaluator_adapter import EvaluatorAdapter


# Paths relative to repo root — adjust if the package moves.
REPO_ROOT = Path(__file__).parent.parent
BASELINE_DIR = REPO_ROOT / "skill_files_baseline"
PPTX_SKILL_DIR = REPO_ROOT / "pptx"
TASK_PROMPT_PATH = REPO_ROOT / "output" / "TASK_PROMPT.md"
REFERENCE_DIR = REPO_ROOT / "output" / "reference"

# Reward capping parameters
REWARD_CLIP_POINTS = 30  # clip score delta to +/-30 before normalizing
REWARD_SCALE = 100.0  # divide clipped delta by this to get [-0.3, +0.3]

MAX_STEPS = int(os.environ.get("SLIDE_SKILL_MAX_STEPS", "7"))

# Session directory root: defaults to repo/tmp/ locally, configurable via
# env var so HuggingFace Spaces (read-only app dir) can use /tmp instead.
_default_session_root = str(REPO_ROOT / "tmp")
SESSION_ROOT = Path(os.environ.get("SLIDE_SKILL_SESSION_ROOT", _default_session_root))

# Baseline skill files (DESIGN_RULES.md + EXAMPLES.md) and generic pptx
# tooling files that get copied into each session.
BASELINE_FILES = ("DESIGN_RULES.md", "EXAMPLES.md")
PPTX_SKILL_FILES = ("SKILL.md", "editing.md", "pptxgenjs.md")


class SlideSkillEnvironment:
    """OpenEnv environment for the Skill Forge optimization loop."""

    SUPPORTS_CONCURRENT_SESSIONS: ClassVar[bool] = True

    def __init__(self) -> None:
        self._sessions: dict[str, SlideSkillState] = {}
        self._generator = SlideGenerator(
            task_prompt_path=TASK_PROMPT_PATH,
            pptx_skill_dir=PPTX_SKILL_DIR,
            reference_dir=REFERENCE_DIR,
        )
        self._evaluator = EvaluatorAdapter(reference_dir=REFERENCE_DIR)

    # ------------------------------------------------------------------
    # Public OpenEnv interface
    # ------------------------------------------------------------------

    def reset(self, session_id: str | None = None) -> str:
        """
        Initialize or reinitialize a session.

        Creates an isolated working directory under /tmp/ and copies both
        the baseline skill files and the generic pptx tooling files into it.
        Returns the session_id.
        """
        session_id = session_id or str(uuid.uuid4())

        session_dir = SESSION_ROOT / f"slide_skill_{session_id}"
        if session_dir.exists():
            shutil.rmtree(session_dir)
        session_dir.mkdir(parents=True)

        # Copy baseline skill files (DESIGN_RULES.md, EXAMPLES.md).
        for fname in BASELINE_FILES:
            src = BASELINE_DIR / fname
            if not src.exists():
                raise FileNotFoundError(
                    f"Baseline file missing: {src}. "
                    "Commit skill_files_baseline/ to the repo."
                )
            shutil.copy2(src, session_dir / fname)

        # Copy generic pptx skill/tooling files so the agent can edit them.
        for fname in PPTX_SKILL_FILES:
            src = PPTX_SKILL_DIR / fname
            if src.exists():
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
            action: Any SlideSkillAction variant.

        Returns:
            SlideSkillObservation with scores, feedback, reward, and file contents.

        Raises:
            KeyError: If session_id is not found.
            RuntimeError: If the generation or evaluation pipeline fails.
        """
        state = self._sessions[session_id]
        session_dir = Path(state.session_dir)

        # 1. Apply the action to the session's skill files / state.
        manager = SkillManager(session_dir, state)
        manager.apply(action)

        # 2. Run the full generation pipeline.
        #    Pass state so the generator can inject templates/constraints
        #    and apply code patches.
        jpg_path = self._generator.generate(
            session_id=session_id,
            session_dir=session_dir,
            state=state,
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
        design_rules = (session_dir / "DESIGN_RULES.md").read_text(encoding="utf-8")
        examples = (session_dir / "EXAMPLES.md").read_text(encoding="utf-8")

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
            js_templates=dict(state.js_templates),
            constraints=list(state.constraints),
            code_patches=list(state.code_patches),
        )

    def close(self, session_id: str) -> None:
        """Clean up session resources. Deletes the /tmp/ session directory."""
        if session_id in self._sessions:
            state = self._sessions.pop(session_id)
            session_dir = Path(state.session_dir)
            if session_dir.exists():
                shutil.rmtree(session_dir)
