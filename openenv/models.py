"""
Pydantic data models for the Slide Skill OpenEnv environment.

Action space:
    SlideSkillAction is a discriminated union of action types:

    File-level actions (modify skill markdown files):
    - EditSectionAction: Replace a named section's body in one skill file.
    - ReplaceFileAction: Replace the entire content of one skill file.

    Structured actions (higher-level operations):
    - AppendExampleAction: Append a scored example entry to EXAMPLES.md.
    - EditJsTemplateAction: Define a reusable JS code block injected into
      the generator prompt as a mandatory snippet.
    - SetConstraintAction: Add or remove a hard constraint for the generator.
    - PatchCodeAction: Add a regex find/replace rule applied to generated JS
      after LLM output but before Node.js execution.

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

SkillFile = Literal[
    "DESIGN_RULES.md",
    "EXAMPLES.md",
    "SKILL.md",
    "editing.md",
    "pptxgenjs.md",
]
"""Skill files the optimizer is allowed to modify."""


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


class AppendExampleAction(BaseModel):
    """
    Append a scored example entry to EXAMPLES.md.

    Builds a memory of what the evaluator rewards, giving the generator
    better few-shot context over time. The entry is formatted as a markdown
    section with score, verdict, and description.
    """

    action_type: Literal["append_example"] = "append_example"
    description: str = Field(
        ...,
        description="What this example demonstrates (e.g. 'White bg with navy table headers').",
    )
    score: int = Field(
        ..., ge=0, le=100,
        description="The score this approach achieved (0-100).",
    )
    verdict: str = Field(
        ...,
        description="Evaluator's one-line verdict for this example.",
    )


class EditJsTemplateAction(BaseModel):
    """
    Define or update a reusable JS code block injected into the generator prompt.

    Templates are stored per-session and injected as a "## Required Code Blocks"
    section. The generator LLM is instructed to use the exact code for the
    named block. Set js_code to empty string to delete a template.

    Example:
        action = EditJsTemplateAction(
            block_name="footer",
            js_code="slide.addText('McKinsey & Company', {x: 8.5, y: 5.2, ...});"
        )
    """

    action_type: Literal["edit_js_template"] = "edit_js_template"
    block_name: str = Field(
        ...,
        description="Name for this code block (e.g. 'footer', 'table_style', 'title_section').",
    )
    js_code: str = Field(
        ...,
        description="JavaScript code snippet. Empty string removes the template.",
    )


class SetConstraintAction(BaseModel):
    """
    Add or remove a hard constraint for the generator LLM.

    Constraints are injected into the generator prompt as a "## Hard Constraints"
    section. Each constraint is a single directive like "NEVER use require('react')"
    or "ALWAYS use a white background".
    """

    action_type: Literal["set_constraint"] = "set_constraint"
    constraint: str = Field(
        ...,
        description="The constraint text (e.g. 'NEVER use colored backgrounds for data slides').",
    )
    active: bool = Field(
        True,
        description="True to add/keep the constraint, False to remove it.",
    )


class PatchCodeAction(BaseModel):
    """
    Add a regex find/replace rule applied to generated JS after LLM output
    but before Node.js execution.

    Patches are applied in insertion order. Useful for mechanical fixes like
    color corrections, font swaps, or removing problematic API calls.
    Set replacement to None to remove a patch by its description.
    """

    action_type: Literal["patch_code"] = "patch_code"
    pattern: str = Field(
        ...,
        description="Regex pattern to search for in the generated JS code.",
    )
    replacement: str = Field(
        ...,
        description="Replacement string (supports regex backreferences like \\1).",
    )
    description: str = Field(
        ...,
        description="Human-readable description of what this patch does.",
    )
    active: bool = Field(
        True,
        description="True to add/keep the patch, False to remove it (matched by description).",
    )


# Discriminated union — action_type is the discriminator field.
SlideSkillAction = Annotated[
    EditSectionAction
    | ReplaceFileAction
    | AppendExampleAction
    | EditJsTemplateAction
    | SetConstraintAction
    | PatchCodeAction,
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
    js_templates: dict[str, str] = Field(
        default_factory=dict,
        description="Active JS templates (block_name → js_code).",
    )
    constraints: list[str] = Field(
        default_factory=list,
        description="Active hard constraints for the generator.",
    )
    code_patches: list[dict[str, str]] = Field(
        default_factory=list,
        description="Active code patches (list of {pattern, replacement, description}).",
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
            "Contains copies of skill files that this session is free to "
            "modify without affecting other sessions."
        ),
    )
    js_templates: dict[str, str] = Field(
        default_factory=dict,
        description="Named JS code blocks injected into generator prompt.",
    )
    constraints: list[str] = Field(
        default_factory=list,
        description="Hard constraints injected into generator prompt.",
    )
    code_patches: list[dict[str, str]] = Field(
        default_factory=list,
        description="Regex patches applied to generated JS post-LLM.",
    )
