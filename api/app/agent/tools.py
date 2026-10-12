"""Per-request tools that let the agent run a skill's bundled script on user-supplied files.

Each chat request gets its own scratch directory. Scripts run with the server's Python,
without a shell, from an allowlist, with that directory as the working directory.
"""

from __future__ import annotations

import asyncio
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Callable

from .. import config
from ..catalog import load_catalog

_SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,99}$")


def safe_filename(name: str) -> str | None:
    """The name if it is a plain file name with no directory part, else None."""
    return name if _SAFE_NAME.match(name or "") else None


def check_args(args: list[str]) -> str | None:
    """An error message when an argument could reach outside the scratch directory."""
    for arg in args:
        if not isinstance(arg, str) or len(arg) > 4000 or "\x00" in arg:
            return "arguments must be strings of at most 4000 characters"
        value = arg.split("=", 1)[1] if arg.startswith("--") and "=" in arg else arg
        if ".." in Path(value).parts or Path(value).is_absolute() or re.match(r"^[A-Za-z]:", value) \
                or value.startswith(("~", "/", "\\")):
            return f"argument {arg!r} is not allowed: file arguments must be plain names in the working folder"
    return None


def _clip(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[:limit] + f"\n… [truncated {len(text) - limit} characters]"


def make_script_tools(workdir: Path, extra_env: dict[str, str] | None = None) -> list[Callable]:
    """Build the write_file, read_file, and run_script tools bound to one scratch directory."""
    catalog = load_catalog()

    def write_file(filename: str, content: str) -> dict:
        """Save text to a file in the working folder so a script can read it.

        Use this to hand a script its input, for example a .bib file, a CSV table, or a
        .tex draft that the user pasted into the chat.

        Args:
            filename: A plain file name such as "refs.bib" or "data.csv". No folders.
            content: The full text of the file.
        """
        if not safe_filename(filename):
            return {"status": "error", "error": "filename must be a plain name such as refs.bib"}
        if len(content) > config.MAX_ATTACHMENT_BYTES:
            return {"status": "error", "error": "content is too large"}
        (workdir / filename).write_text(content, encoding="utf-8")
        return {"status": "ok", "filename": filename, "characters": len(content)}

    def read_file(filename: str) -> dict:
        """Read a text file from the working folder, such as one a script wrote with --out.

        Args:
            filename: A plain file name in the working folder.
        """
        if not safe_filename(filename) or not (workdir / filename).is_file():
            files = sorted(p.name for p in workdir.iterdir() if p.is_file())
            return {"status": "error", "error": f"no such file. Files in the working folder: {files}"}
        text = (workdir / filename).read_text(encoding="utf-8", errors="replace")
        return {"status": "ok", "filename": filename, "content": _clip(text, config.READ_FILE_CHARS)}

    async def run_script(skill_name: str, script: str, args: list[str]) -> dict:
        """Run a Python script that ships with a skill and return what it printed.

        Load the skill first to learn the script's arguments. File arguments refer to
        files in the working folder: files the user attached, or ones saved with write_file.

        Args:
            skill_name: The skill that owns the script, for example "paper-search".
            script: The script file name, for example "search_papers.py".
            args: Command-line arguments, one list item per argument, for example
                ["retrieval augmented generation", "--limit", "10", "--format", "md"].
        """
        entry = catalog.get(skill_name)
        script = (script or "").replace("\\", "/").rsplit("/", 1)[-1]
        if entry is None:
            return {"status": "error", "error": f"unknown skill {skill_name!r}"}
        if script not in entry.scripts:
            return {"status": "error",
                    "error": f"{skill_name} has no runnable script {script!r}. Runnable: {list(entry.scripts)}"}
        problem = check_args(args)
        if problem:
            return {"status": "error", "error": problem}

        env = {k: v for k, v in os.environ.items()
               if k.upper() in ("PATH", "SYSTEMROOT", "TEMP", "TMP", "TMPDIR", "LANG", "LD_LIBRARY_PATH",
                                "PYTHONPATH", "OPENALEX_MAILTO")}
        env.update({"PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1", "HOME": str(workdir),
                    **(extra_env or {})})
        command = [sys.executable, "-B", str(entry.directory / "scripts" / script), *args]
        try:
            done = await asyncio.to_thread(
                subprocess.run, command, cwd=workdir, env=env, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=config.SCRIPT_TIMEOUT_SECONDS,
                stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            return {"status": "error", "error": f"script timed out after {config.SCRIPT_TIMEOUT_SECONDS} seconds"}
        return {
            "status": "ok" if done.returncode == 0 else "error",
            "exit_code": done.returncode,
            "stdout": _clip(done.stdout, config.SCRIPT_OUTPUT_CHARS),
            "stderr": _clip(done.stderr, 4000),
            "files": sorted(p.name for p in workdir.iterdir() if p.is_file()),
        }

    return [write_file, read_file, run_script]
