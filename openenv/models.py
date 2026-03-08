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

from typing import Annotated, Literal

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
    """Raw scores from the McKinsey evaluator. Each dimension is 0-15 except
    overall_impression which is 0-10. Total is 0-100."""

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
    total: int = Field(..., description="Sum of all score dimensions (0-100).")
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
