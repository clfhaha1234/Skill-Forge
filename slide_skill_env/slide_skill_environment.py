"""Main OpenEnv environment — orchestrates optimize -> generate -> evaluate."""

import base64
import shutil
import tempfile
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

import os
from dotenv import load_dotenv

load_dotenv()

from slide_skill_env.converter import pptx_to_jpg
from slide_skill_env.evaluator import evaluate_slide
from slide_skill_env.generator import generate_slide
from slide_skill_env.models import SkillAction, SkillObservation, SkillState
from slide_skill_env.optimizer import optimize_skill
from slide_skill_env.skill_manager import SkillManager


class SlideSkillEnvironment:
    """OpenEnv environment for self-improving PPT skill optimization."""

    SUPPORTS_CONCURRENT_SESSIONS = False

    def __init__(self):
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
        self._cleanup()

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

        # Run initial generate -> evaluate to get baseline score
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
        """Run one optimize -> generate -> convert -> evaluate cycle."""
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
        reward = max(-0.3, min(0.3, reward))
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
        history = self._state.score_history
        step = self._state.step_count

        if step >= self._state.max_steps:
            return True, "max_steps"

        if history and history[-1] >= self._state.score_threshold:
            return True, "threshold"

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
