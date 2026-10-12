"""The skill catalog: the 59 vendored skills, loaded once and shared by the API and the agent."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from google.adk.skills import load_skill_from_dir
from google.adk.skills.models import Skill

from .config import SKILLS_DIR

# Scripts that cannot work in a stateless serverless function: pubstyle needs matplotlib,
# log_run keeps a notebook on disk and shells out to git.
BLOCKED_SCRIPTS = {"pubstyle.py", "log_run.py"}


@dataclass(frozen=True)
class SkillEntry:
    name: str
    title: str
    description: str
    summary: str
    stage: str
    stage_index: int
    tags: tuple[str, ...]
    scripts: tuple[str, ...]
    references: tuple[str, ...]
    markdown: str
    skill: Skill
    directory: Path

    def brief(self) -> dict:
        return {
            "name": self.name, "title": self.title, "description": self.description,
            "summary": self.summary, "stage": self.stage, "stage_index": self.stage_index,
            "tags": list(self.tags), "scripts": list(self.scripts),
        }

    def detail(self) -> dict:
        return {**self.brief(), "references": list(self.references), "markdown": self.markdown}


def _title(markdown: str, name: str) -> str:
    match = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE)
    return match.group(1).strip() if match else name.replace("-", " ").title()


def _runnable_scripts(directory: Path) -> tuple[str, ...]:
    scripts = directory / "scripts"
    if not scripts.is_dir():
        return ()
    return tuple(sorted(p.name for p in scripts.glob("*.py")
                        if not p.name.startswith("_") and p.name not in BLOCKED_SCRIPTS))


@lru_cache(maxsize=1)
def load_catalog() -> dict[str, SkillEntry]:
    """Every skill by name, in lifecycle order."""
    stages: dict[str, dict[str, str]] = json.loads((SKILLS_DIR / "catalog.json").read_text(encoding="utf-8"))
    entries: dict[str, SkillEntry] = {}
    for stage_index, (stage_label, skills) in enumerate(stages.items(), 1):
        stage = re.sub(r"^\d+\.\s*", "", stage_label)
        for name, summary in skills.items():
            directory = SKILLS_DIR / name
            skill = load_skill_from_dir(directory)
            metadata = skill.frontmatter.metadata or {}
            entries[name] = SkillEntry(
                name=name,
                title=_title(skill.instructions, name),
                description=skill.frontmatter.description,
                summary=summary,
                stage=stage,
                stage_index=stage_index,
                tags=tuple(metadata.get("tags") or ()),
                scripts=_runnable_scripts(directory),
                references=tuple(sorted(
                    f"{folder}/{p.name}" for folder in ("references", "assets")
                    for p in (directory / folder).glob("*") if p.is_file())),
                markdown=skill.instructions,
                skill=skill,
                directory=directory,
            )
    return entries


def stages() -> list[dict]:
    """Lifecycle stages in order, each with its skill count."""
    out: dict[int, dict] = {}
    for entry in load_catalog().values():
        stage = out.setdefault(entry.stage_index, {"index": entry.stage_index, "name": entry.stage, "count": 0})
        stage["count"] += 1
    return [out[i] for i in sorted(out)]
