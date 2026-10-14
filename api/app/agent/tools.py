"""Tools that run skill scripts and read/write the per-request working folder."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Callable

from .. import config
from ..catalog import load_catalog

SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,199}$")
# Drop LLM and cloud credentials so a script cannot send the user's key elsewhere.
_STRIP_ENV = {
    "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY", "GEMINI_API_KEY",
    "GROQ_API_KEY", "OPENROUTER_API_KEY", "NVIDIA_API_KEY", "AZURE_OPENAI_API_KEY",
    "AZURE_API_KEY", "AWS_SECRET_ACCESS_KEY", "AWS_ACCESS_KEY_ID", "AWS_SESSION_TOKEN",
    "MISTRAL_API_KEY", "COHERE_API_KEY", "TOGETHER_API_KEY", "FIREWORKS_API_KEY",
    "XAI_API_KEY", "DEEPSEEK_API_KEY",
}


def _outside_workdir(arg: str) -> bool:
    """True when an argument could point outside the private working folder."""
    if "\x00" in arg:
        return True
    value = arg.split("=", 1)[1] if arg.startswith("--") and "=" in arg else arg
    return (
        ".." in Path(value).parts
        or Path(value).is_absolute()
        or value.startswith(("~", "/", "\\"))
        or bool(re.match(r"^[A-Za-z]:", value))
    )


def safe_filename(name: str) -> bool:
    return bool(name and SAFE_NAME.match(name) and "/" not in name and "\\" not in name and ".." not in name)


def _clip(text: str, limit: int = config.SCRIPT_OUTPUT_CHARS) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n… truncated after {limit} characters"


def make_script_tools(workdir: Path, script_env: dict[str, str] | None = None) -> list[Callable]:
    """Return run_script, write_file, and read_file bound to one working folder."""
    workdir = workdir.resolve()
    extra_env = {k: v for k, v in (script_env or {}).items() if v}

    def run_script(skill_name: str, script: str, args: list[str] | None = None) -> dict:
        """Run a Python script that ships with a skill.

        Args:
            skill_name: Skill folder name, for example paper-search.
            script: Filename in that skill's scripts/ folder, for example search_papers.py.
            args: Command-line arguments as a list of strings. Do not concatenate them.
        """
        catalog = load_catalog()
        if skill_name not in catalog:
            return {"status": "error", "error": f"unknown skill '{skill_name}'"}
        if skill_name in config.UNAVAILABLE_SCRIPTS:
            return {"status": "error", "error": config.UNAVAILABLE_SCRIPTS[skill_name]}
        # Models often copy the path from SKILL.md ("scripts/x.py"); the folder is implied.
        script = script.removeprefix("scripts/").removeprefix("scripts\\")
        if not safe_filename(script) or not script.endswith(".py") or script.startswith("_"):
            return {"status": "error", "error": "script name is not allowed"}
        script_path = (catalog[skill_name].path / "scripts" / script).resolve()
        scripts_root = (catalog[skill_name].path / "scripts").resolve()
        if not str(script_path).startswith(str(scripts_root) + os.sep) or not script_path.is_file():
            return {"status": "error", "error": f"'{script}' is not a script of {skill_name}"}
        argv = [str(a) for a in (args or [])]
        if len(argv) > 40 or any(len(a) > 4000 for a in argv):
            return {"status": "error", "error": "too many or too long script arguments"}
        unsafe = next((arg for arg in argv if _outside_workdir(arg)), None)
        if unsafe:
            return {
                "status": "error",
                "error": f"argument {unsafe!r} is not allowed: file arguments must stay in the working folder",
            }

        env = {k: v for k, v in os.environ.items() if k not in _STRIP_ENV}
        env.update(extra_env)
        # Serverless runtimes add the installed packages to sys.path at startup rather than
        # through PYTHONPATH, so hand the child the same path or numpy/scipy won't import.
        inherited = [p for p in sys.path if p and os.path.isdir(p)]
        env["PYTHONPATH"] = os.pathsep.join([str(scripts_root), *inherited, env.get("PYTHONPATH", "")])
        env["PYTHONUNBUFFERED"] = "1"
        try:
            completed = subprocess.run(
                [sys.executable, str(script_path), *argv],
                cwd=workdir,
                env=env,
                capture_output=True,
                text=True,
                timeout=config.SCRIPT_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "error": f"script timed out after {config.SCRIPT_TIMEOUT_SECONDS}s",
            }
        except OSError as exc:
            return {"status": "error", "error": f"could not run script: {exc}"}
        result = {
            "status": "ok" if completed.returncode == 0 else "error",
            "exit_code": completed.returncode,
            "stdout": _clip(completed.stdout or ""),
            "stderr": _clip(completed.stderr or ""),
        }
        if completed.returncode != 0:
            result["error"] = f"{script} exited {completed.returncode}"
        return result

    def write_file(filename: str, content: str) -> dict:
        """Write a text file into the private working folder for scripts to read.

        Args:
            filename: A simple file name (letters, digits, dot, dash, underscore).
            content: The full text to write.
        """
        if not safe_filename(filename):
            return {"status": "error", "error": "filename is not allowed"}
        if len(content) > config.MAX_ATTACHMENT_BYTES:
            return {"status": "error", "error": "file is too large"}
        path = workdir / filename
        path.write_text(content, encoding="utf-8")
        return {"status": "ok", "filename": filename, "bytes": path.stat().st_size}

    def read_file(filename: str) -> dict:
        """Read a text file from the private working folder.

        Args:
            filename: A simple file name previously written or produced by a script.
        """
        if not safe_filename(filename):
            return {"status": "error", "error": "filename is not allowed"}
        path = workdir / filename
        if not path.is_file():
            return {"status": "error", "error": f"'{filename}' does not exist"}
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return {"status": "error", "error": f"'{filename}' is not text"}
        return {"status": "ok", "filename": filename, "content": _clip(text, config.READ_FILE_CHARS)}

    return [run_script, write_file, read_file]
