#!/usr/bin/env python3
"""Vendor the research-scholar skills into api/skills at a pinned upstream commit.

    python scripts/sync_skills.py            # use the pinned commit
    python scripts/sync_skills.py --ref main # move to another ref, then update PINNED_REF

Copies every skills/<name>/ folder (without its evals/) and tools/catalog.json.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

UPSTREAM = "https://github.com/Yash-Kavaiya/research-scholar-agent-skills"
PINNED_REF = "856545ecda8ce125d405eb63b0343ccaa20e178b"
TARGET = Path(__file__).resolve().parent.parent / "api" / "skills"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ref", default=PINNED_REF, help="upstream commit, tag, or branch")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        clone = Path(tmp) / "upstream"
        subprocess.run(["git", "clone", "--quiet", UPSTREAM, str(clone)], check=True)
        subprocess.run(["git", "-C", str(clone), "checkout", "--quiet", args.ref], check=True)
        commit = subprocess.run(["git", "-C", str(clone), "rev-parse", "HEAD"], check=True,
                                capture_output=True, text=True).stdout.strip()

        if TARGET.exists():
            shutil.rmtree(TARGET)
        TARGET.mkdir(parents=True)
        count = 0
        for skill in sorted((clone / "skills").iterdir()):
            if not (skill / "SKILL.md").is_file():
                continue
            shutil.copytree(skill, TARGET / skill.name,
                            ignore=shutil.ignore_patterns("evals", "__pycache__", "*.pyc"))
            count += 1
        shutil.copy2(clone / "tools" / "catalog.json", TARGET / "catalog.json")
        (TARGET / "UPSTREAM").write_text(f"{UPSTREAM}\n{commit}\n", encoding="utf-8")

    print(f"vendored {count} skills at {commit} into {TARGET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
