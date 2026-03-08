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
