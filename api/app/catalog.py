"""Reads the skill library from disk. Used by the catalog API and by the agent factory."""

from __future__ import annotations

import functools
from dataclasses import dataclass, field
from pathlib import Path

from .config import SKILLS_DIR

STAGES: list[tuple[str, str]] = [
    ("problem", "Finding a problem"),
    ("literature", "Literature discovery and reading"),
    ("review", "Literature review"),
    ("design", "Research design and methodology"),
    ("analysis", "Experiments and analysis"),
    ("writing", "Writing"),
    ("figures", "Figures and tables"),
    ("citations", "Citations and integrity"),
    ("submission", "Submission and peer review"),
    ("funding", "Funding and career"),
    ("dissemination", "Dissemination"),
    ("orchestrators", "Orchestrators"),
]

# Folder name → stage id. Kept here so the HTTP catalog does not depend on ADK.
SKILL_STAGE: dict[str, str] = {
    "research-gap-finder": "problem",
    "research-question-formulator": "problem",
    "novelty-checker": "problem",
    "topic-trend-analyzer": "problem",
    "paper-search": "literature",
    "citation-graph-explorer": "literature",
    "paper-summarizer": "literature",
    "paper-critic": "literature",
    "paper-comparison-matrix": "literature",
    "math-and-equation-explainer": "literature",
    "systematic-review-prisma": "review",
    "literature-review-writer": "review",
    "related-work-writer": "review",
    "annotated-bibliography-builder": "review",
    "methodology-designer": "design",
    "experiment-planner": "design",
    "sample-size-power-calculator": "design",
    "survey-questionnaire-designer": "design",
    "dataset-finder": "design",
    "ethics-irb-drafter": "design",
    "paper-to-code-reproducer": "analysis",
    "statistical-test-selector": "analysis",
    "results-interpreter": "analysis",
    "ablation-study-designer": "analysis",
    "qualitative-coding-assistant": "analysis",
    "experiment-logger": "analysis",
    "paper-outline-generator": "writing",
    "abstract-writer": "writing",
    "introduction-writer": "writing",
    "academic-tone-editor": "writing",
    "latex-paper-formatter": "writing",
    "thesis-chapter-writer": "writing",
    "limitations-and-future-work-writer": "writing",
    "publication-figure-maker": "figures",
    "architecture-diagram-maker": "figures",
    "latex-table-generator": "figures",
    "citation-verifier": "citations",
    "bibtex-manager": "citations",
    "citation-style-converter": "citations",
    "plagiarism-and-paraphrase-checker": "citations",
    "reproducibility-checklist": "citations",
    "venue-recommender": "submission",
    "self-peer-reviewer": "submission",
    "rebuttal-writer": "submission",
    "cover-letter-writer": "submission",
    "camera-ready-checker": "submission",
    "grant-proposal-writer": "funding",
    "phd-research-proposal-writer": "funding",
    "sop-and-research-statement-writer": "funding",
    "supervisor-finder": "funding",
    "paper-to-slides": "dissemination",
    "paper-to-poster": "dissemination",
    "paper-to-blog": "dissemination",
    "paper-to-explainer-video": "dissemination",
    "viva-defense-prep": "dissemination",
    "research-scholar-orchestrator": "orchestrators",
    "idea-to-paper-pipeline": "orchestrators",
    "weekly-paper-digest": "orchestrators",
    "research-progress-tracker": "orchestrators",
}

_STAGE_NAME = dict(STAGES)
_STAGE_NUMBER = {sid: i + 1 for i, (sid, _) in enumerate(STAGES)}


@dataclass(frozen=True)
class SkillEntry:
    name: str
    description: str
    stage: str
    body: str
    tags: list[str] = field(default_factory=list)
    scripts: list[str] = field(default_factory=list)
    compatibility: str | None = None
    path: Path = field(default=SKILLS_DIR)

    @property
    def stage_name(self) -> str:
        return _STAGE_NAME.get(self.stage, "Other")

    @property
    def stage_number(self) -> int:
        return _STAGE_NUMBER.get(self.stage, 0)


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    rest = text[3:]
    end = rest.find("\n---")
    if end < 0:
        return {}, text
    raw, body = rest[:end], rest[end + 4 :]
    data: dict = {}
    try:
        import yaml  # shipped with google-adk

        parsed = yaml.safe_load(raw) or {}
        if isinstance(parsed, dict):
            data = parsed
    except Exception:
        data = {}
    return data, body.lstrip("\n")


def _scripts(folder: Path) -> list[str]:
    scripts_dir = folder / "scripts"
    if not scripts_dir.is_dir():
        return []
    names = []
    for path in sorted(scripts_dir.iterdir()):
        if path.suffix == ".py" and path.is_file() and not path.name.startswith("_"):
            names.append(path.name)
    return names


@functools.lru_cache(maxsize=1)
def load_catalog() -> dict[str, SkillEntry]:
    catalog: dict[str, SkillEntry] = {}
    if not SKILLS_DIR.is_dir():
        return catalog
    for folder in sorted(SKILLS_DIR.iterdir()):
        skill_md = folder / "SKILL.md"
        if not folder.is_dir() or not skill_md.is_file():
            continue
        meta, body = _parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        name = str(meta.get("name") or folder.name).strip()
        description = str(meta.get("description") or "").strip()
        tags: list[str] = []
        metadata = meta.get("metadata") or {}
        if isinstance(metadata, dict) and isinstance(metadata.get("tags"), list):
            tags = [str(t) for t in metadata["tags"]]
        catalog[name] = SkillEntry(
            name=name,
            description=description,
            stage=SKILL_STAGE.get(name, "orchestrators"),
            body=body,
            tags=tags,
            scripts=_scripts(folder),
            compatibility=(str(meta["compatibility"]) if meta.get("compatibility") else None),
            path=folder,
        )
    return catalog


def stages_payload() -> list[dict]:
    return [
        {"id": sid, "name": name, "number": i + 1}
        for i, (sid, name) in enumerate(STAGES)
    ]


def skill_summary(entry: SkillEntry) -> dict:
    return {
        "name": entry.name,
        "description": entry.description,
        "stage": entry.stage,
        "stageName": entry.stage_name,
        "stageNumber": entry.stage_number,
        "tags": entry.tags,
        "scripts": entry.scripts,
        "hasScripts": bool(entry.scripts),
    }


def skill_detail(entry: SkillEntry) -> dict:
    return {**skill_summary(entry), "body": entry.body, "compatibility": entry.compatibility}
