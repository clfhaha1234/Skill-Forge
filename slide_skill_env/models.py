"""Pydantic models for the Slide Skill OpenEnv environment."""

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
