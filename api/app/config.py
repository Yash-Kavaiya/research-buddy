"""Static configuration: LLM providers, request limits, and paths."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"

# Request limits. The body limit stays under Vercel's 4.5 MB request cap.
MAX_MESSAGE_CHARS = 30_000
MAX_HISTORY_TURNS = 60
MAX_HISTORY_CHARS = 400_000
MAX_ATTACHMENTS = 5
MAX_ATTACHMENT_BYTES = 3_000_000
MAX_LLM_CALLS = 30

# Script execution limits.
SCRIPT_TIMEOUT_SECONDS = 90
SCRIPT_OUTPUT_CHARS = 24_000
READ_FILE_CHARS = 24_000

# Best-effort per-IP limit on chat requests (per serverless instance).
RATE_LIMIT_REQUESTS = int(os.environ.get("RATE_LIMIT_REQUESTS", "30"))
RATE_LIMIT_WINDOW_SECONDS = 60


@dataclass(frozen=True)
class Provider:
    id: str
    name: str
    litellm_prefix: str
    key_hint: str
    key_url: str
    models_url: str

    def litellm_model(self, model: str) -> str:
        return f"{self.litellm_prefix}/{model}"


# No model names are listed here on purpose: providers retire models often, so the
# app asks the provider which models the caller's key can use (GET /api/models).
PROVIDERS: dict[str, Provider] = {p.id: p for p in [
    Provider("google", "Google Gemini", "gemini", "AIza…", "https://aistudio.google.com/apikey",
             "https://generativelanguage.googleapis.com/v1beta/models?pageSize=1000"),
    Provider("openai", "OpenAI", "openai", "sk-…", "https://platform.openai.com/api-keys",
             "https://api.openai.com/v1/models"),
    Provider("anthropic", "Anthropic", "anthropic", "sk-ant-…", "https://console.anthropic.com/settings/keys",
             "https://api.anthropic.com/v1/models?limit=1000"),
    Provider("groq", "Groq", "groq", "gsk_…", "https://console.groq.com/keys",
             "https://api.groq.com/openai/v1/models"),
    Provider("openrouter", "OpenRouter", "openrouter", "sk-or-…", "https://openrouter.ai/keys",
             "https://openrouter.ai/api/v1/models"),
    Provider("nvidia", "NVIDIA NIM", "nvidia_nim", "nvapi-…", "https://build.nvidia.com/settings/api-keys",
             "https://integrate.api.nvidia.com/v1/models"),
]}
