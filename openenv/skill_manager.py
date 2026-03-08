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
            self._replace_file(target, action)  # type: ignore[arg-type]
        elif action.action_type == "edit_section":
            self._edit_section(target, action)  # type: ignore[arg-type]
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
            + lines[end_idx:]  # rest of file after the section
        )
        target.write_text("".join(new_lines), encoding="utf-8")

    def read_file(self, filename: str) -> str:
        """Read a skill file from the session directory."""
        return (self.session_dir / filename).read_text(encoding="utf-8")
