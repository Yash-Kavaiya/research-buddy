"""Static configuration: LLM providers, request limits, and paths."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"

# Stay under Vercel's 4.5 MB request cap.
MAX_MESSAGE_CHARS = 30_000
MAX_HISTORY_TURNS = 60
MAX_HISTORY_CHARS = 400_000
MAX_ATTACHMENTS = 5
MAX_ATTACHMENT_BYTES = 3_000_000
MAX_LLM_CALLS = 30

SCRIPT_TIMEOUT_SECONDS = 90
SCRIPT_OUTPUT_CHARS = 24_000
READ_FILE_CHARS = 24_000

RATE_LIMIT_REQUESTS = int(os.environ.get("RATE_LIMIT_REQUESTS", "30"))
RATE_LIMIT_WINDOW_SECONDS = 60

# Scripts that need local packages or a researcher's own machine.
UNAVAILABLE_SCRIPTS = {
    "publication-figure-maker": (
        "publication-figure-maker's plotting scripts are not installed on this server. "
        "Give the user the matplotlib or TikZ code to run locally."
    ),
    "experiment-logger": (
        "experiment-logger's lab-notebook scripts are meant to run on the researcher's machine. "
        "Give them the commands to run locally."
    ),
}


@dataclass(frozen=True)
class Provider:
    id: str
    name: str
    litellm_prefix: str
    key_hint: str
    key_url: str
    models: list[str] = field(default_factory=list)

    def litellm_model(self, model: str) -> str:
        return f"{self.litellm_prefix}/{model}"


# `models` are suggestions shown in the UI; any model id the provider serves can be typed in.
PROVIDERS: dict[str, Provider] = {p.id: p for p in [
    Provider("google", "Google Gemini", "gemini", "AIza…", "https://aistudio.google.com/apikey",
             ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.5-flash-lite"]),
    Provider("openai", "OpenAI", "openai", "sk-…", "https://platform.openai.com/api-keys",
             ["gpt-4.1", "gpt-4.1-mini", "gpt-4o"]),
    Provider("anthropic", "Anthropic", "anthropic", "sk-ant-…",
             "https://console.anthropic.com/settings/keys",
             ["claude-sonnet-4-5", "claude-opus-4-5", "claude-haiku-4-5"]),
    Provider("groq", "Groq", "groq", "gsk_…", "https://console.groq.com/keys",
             ["llama-3.3-70b-versatile", "openai/gpt-oss-120b"]),
    Provider("openrouter", "OpenRouter", "openrouter", "sk-or-…", "https://openrouter.ai/keys",
             ["google/gemini-2.5-flash", "anthropic/claude-sonnet-4.5", "openai/gpt-4.1"]),
    Provider("nvidia", "NVIDIA NIM", "nvidia_nim", "nvapi-…",
             "https://build.nvidia.com/settings/api-keys",
             ["meta/llama-3.3-70b-instruct", "nvidia/llama-3.3-nemotron-super-49b-v1.5"]),
]}
