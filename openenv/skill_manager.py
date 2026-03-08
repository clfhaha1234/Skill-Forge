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

from models import (
    AppendExampleAction,
    EditJsTemplateAction,
    EditSectionAction,
    PatchCodeAction,
    ReplaceFileAction,
    SetConstraintAction,
    SlideSkillAction,
    SlideSkillState,
)


class SkillManager:
    """Manages skill files and structured state within a session directory."""

    def __init__(self, session_dir: Path, state: SlideSkillState) -> None:
        self.session_dir = session_dir
        self.state = state

    def apply(self, action: SlideSkillAction) -> None:
        """
        Dispatch to the appropriate handler based on action type.

        Raises:
            ValueError: If action_type is unrecognized or section not found.
            FileNotFoundError: If the target skill file does not exist.
        """
        if action.action_type == "replace_file":
            target = self.session_dir / action.file
            if not target.exists():
                raise FileNotFoundError(f"Skill file not found in session: {target}")
            self._replace_file(target, action)  # type: ignore[arg-type]
        elif action.action_type == "edit_section":
            target = self.session_dir / action.file
            if not target.exists():
                raise FileNotFoundError(f"Skill file not found in session: {target}")
            self._edit_section(target, action)  # type: ignore[arg-type]
        elif action.action_type == "append_example":
            self._append_example(action)  # type: ignore[arg-type]
        elif action.action_type == "edit_js_template":
            self._edit_js_template(action)  # type: ignore[arg-type]
        elif action.action_type == "set_constraint":
            self._set_constraint(action)  # type: ignore[arg-type]
        elif action.action_type == "patch_code":
            self._patch_code(action)  # type: ignore[arg-type]
        else:
            raise ValueError(f"Unknown action_type: {action.action_type!r}")

    # ------------------------------------------------------------------
    # File-level actions
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
            + lines[end_idx:]  # rest of file after the section
        )
        target.write_text("".join(new_lines), encoding="utf-8")

    # ------------------------------------------------------------------
    # Structured actions
    # ------------------------------------------------------------------

    def _append_example(self, action: AppendExampleAction) -> None:
        """Append a scored example entry to EXAMPLES.md."""
        examples_path = self.session_dir / "EXAMPLES.md"
        current = examples_path.read_text(encoding="utf-8")

        entry = (
            f"\n## Example (score: {action.score}/100)\n"
            f"**Verdict:** {action.verdict}\n\n"
            f"{action.description}\n"
        )
        examples_path.write_text(current + entry, encoding="utf-8")

    def _edit_js_template(self, action: EditJsTemplateAction) -> None:
        """Add, update, or remove a named JS template block."""
        if action.js_code:
            self.state.js_templates[action.block_name] = action.js_code
        else:
            self.state.js_templates.pop(action.block_name, None)

    def _set_constraint(self, action: SetConstraintAction) -> None:
        """Add or remove a hard constraint."""
        if action.active:
            if action.constraint not in self.state.constraints:
                self.state.constraints.append(action.constraint)
        else:
            self.state.constraints = [
                c for c in self.state.constraints if c != action.constraint
            ]

    def _patch_code(self, action: PatchCodeAction) -> None:
        """Add or remove a code patch."""
        if action.active:
            # Remove existing patch with same description before adding.
            self.state.code_patches = [
                p for p in self.state.code_patches
                if p["description"] != action.description
            ]
            self.state.code_patches.append({
                "pattern": action.pattern,
                "replacement": action.replacement,
                "description": action.description,
            })
        else:
            self.state.code_patches = [
                p for p in self.state.code_patches
                if p["description"] != action.description
            ]

    def read_file(self, filename: str) -> str:
        """Read a skill file from the session directory."""
        return (self.session_dir / filename).read_text(encoding="utf-8")
