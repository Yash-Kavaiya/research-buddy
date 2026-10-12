from __future__ import annotations

import sys
from pathlib import Path
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.agent import factory  # noqa: E402
from app.main import app  # noqa: E402
from app.routers import chat  # noqa: E402

HEADERS = {"X-LLM-Provider": "openai", "X-LLM-Model": "gpt-test", "X-LLM-Key": "sk-test-SECRET-1234567890"}


class ScriptedLlm(BaseLlm):
    """A model that replays a fixed list of responses, one per call, and records what it was sent."""

    steps: list = []
    requests: list = []

    async def generate_content_async(self, llm_request: LlmRequest, stream: bool = False
                                     ) -> AsyncGenerator[LlmResponse, None]:
        self.requests.append(llm_request)
        step = self.steps.pop(0)
        if isinstance(step, Exception):
            raise step
        yield LlmResponse(content=types.Content(role="model", parts=[step]))


def call(name: str, **args) -> types.Part:
    return types.Part(function_call=types.FunctionCall(name=name, args=args, id=f"call-{name}"))


def text(value: str) -> types.Part:
    return types.Part(text=value)


@pytest.fixture
def client() -> TestClient:
    chat._hits.clear()
    return TestClient(app)


@pytest.fixture
def scripted(monkeypatch):
    """Replace the real model with a ScriptedLlm; returns a function that sets its steps."""
    model = ScriptedLlm(model="scripted")
    model.steps, model.requests = [], []
    monkeypatch.setattr(factory, "build_model", lambda provider, name, key: model)

    def use(*steps):
        model.steps[:] = steps
        return model
    return use


def events(response) -> list[dict]:
    import json
    return [json.loads(line[6:]) for line in response.text.splitlines() if line.startswith("data: ")]
