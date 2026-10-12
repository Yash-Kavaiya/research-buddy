#!/usr/bin/env python3
"""Copy skills from the upstream research-scholar-agent-skills repository."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "api" / "skills"
UPSTREAM = "https://github.com/Yash-Kavaiya/research-scholar-agent-skills.git"
SKIP_DIR_NAMES = {".git", "__pycache__", "evals", ".pytest_cache"}


def copy_skills(src: Path, dest: Path) -> int:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    count = 0
    for skill in sorted(src.iterdir()):
        if not skill.is_dir() or not (skill / "SKILL.md").exists():
            continue

        def ignore(dirpath: str, names: list[str]) -> list[str]:
            return [n for n in names if n in SKIP_DIR_NAMES or n.endswith(".pyc")]

        shutil.copytree(skill, dest / skill.name, ignore=ignore)
        count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from", dest="source", help="Local checkout of the upstream repo")
    parser.add_argument("--ref", default="HEAD", help="Git ref to clone when --from is omitted")
    args = parser.parse_args()

    if args.source:
        src = Path(args.source) / "skills"
        sha = subprocess.check_output(["git", "-C", args.source, "rev-parse", "HEAD"], text=True).strip()
        count = copy_skills(src, DEST)
    else:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.check_call(["git", "clone", "--depth", "1", UPSTREAM, tmp])
            sha = subprocess.check_output(["git", "-C", tmp, "rev-parse", "HEAD"], text=True).strip()
            count = copy_skills(Path(tmp) / "skills", DEST)

    (DEST / "UPSTREAM").write_text(f"{UPSTREAM.removesuffix('.git')}\n{sha}\n")
    print(f"copied {count} skills at {sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
