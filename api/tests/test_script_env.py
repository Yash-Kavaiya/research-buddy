from __future__ import annotations

import subprocess
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.agent.tools import make_script_tools


def test_scripts_do_not_inherit_server_secrets(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("VERCEL_OIDC_TOKEN", "oidc-secret")
    monkeypatch.setenv("SOME_SECRET", "s3cret")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-server")
    seen: dict = {}

    def fake_run(argv, **kwargs):
        seen.update(kwargs["env"])
        return subprocess.CompletedProcess(argv, 0, "", "")

    run_script = make_script_tools(tmp_path, {"S2_API_KEY": "s2-user"})[0]
    with patch("app.agent.tools.subprocess.run", fake_run):
        result = run_script("sample-size-power-calculator", "power_calc.py", ["ttest-ind"])
    assert result["status"] == "ok"
    assert "VERCEL_OIDC_TOKEN" not in seen
    assert "SOME_SECRET" not in seen
    assert "OPENAI_API_KEY" not in seen
    assert seen["S2_API_KEY"] == "s2-user"
    assert "PATH" in seen and "PYTHONPATH" in seen


def test_chat_error_redacts_openalex_email(client: TestClient) -> None:
    async def failing_turn(*_args, **_kwargs):
        raise RuntimeError("upstream failed for me@uni.edu")
        yield  # pragma: no cover

    with patch("app.routers.chat.factory.build_agent") as build, patch(
        "app.routers.chat.run_turn", failing_turn
    ):
        build.return_value = object()
        response = client.post(
            "/api/chat",
            json={"message": "hi"},
            headers={
                "X-LLM-Provider": "google", "X-LLM-Model": "gemini-2.5-flash",
                "X-LLM-Key": "sk-test", "X-OpenAlex-Email": "me@uni.edu",
            },
        )
    assert "event: error" in response.text
    assert "me@uni.edu" not in response.text
