from __future__ import annotations

from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.catalog import load_catalog
from app.config import PROVIDERS


def test_health(client: TestClient) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["skills"] == 59


def test_skills_catalog(client: TestClient) -> None:
    response = client.get("/api/skills")
    assert response.status_code == 200
    body = response.json()
    assert len(body["stages"]) == 12
    names = {s["name"] for s in body["skills"]}
    assert "paper-search" in names
    assert "research-scholar-orchestrator" in names
    assert len(body["skills"]) == 59
    paper = next(s for s in body["skills"] if s["name"] == "paper-search")
    assert paper["hasScripts"] is True
    assert paper["stage"] == "literature"


def test_skill_detail(client: TestClient) -> None:
    response = client.get("/api/skills/paper-search")
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "paper-search"
    assert "arXiv" in body["body"]
    assert "search_papers.py" in body["scripts"]


def test_unknown_skill(client: TestClient) -> None:
    response = client.get("/api/skills/not-a-skill")
    assert response.status_code == 404
    assert "message" in response.json()


def test_providers(client: TestClient) -> None:
    response = client.get("/api/providers")
    assert response.status_code == 200
    ids = [p["id"] for p in response.json()["providers"]]
    assert ids == list(PROVIDERS)
    assert all("keyUrl" in p and "models" in p for p in response.json()["providers"])


def test_chat_requires_key(client: TestClient) -> None:
    response = client.post("/api/chat", json={"message": "hello"})
    assert response.status_code == 401
    assert "API key" in response.json()["message"]


def test_chat_unknown_provider(client: TestClient) -> None:
    response = client.post(
        "/api/chat",
        json={"message": "hello"},
        headers={"X-LLM-Provider": "acme", "X-LLM-Model": "x", "X-LLM-Key": "k"},
    )
    assert response.status_code == 400


def test_chat_unknown_skill(client: TestClient) -> None:
    response = client.post(
        "/api/chat",
        json={"message": "hello", "skill": "nope"},
        headers={"X-LLM-Provider": "google", "X-LLM-Model": "gemini-2.5-flash", "X-LLM-Key": "k"},
    )
    assert response.status_code == 422


def test_chat_rejects_bad_attachment_name(client: TestClient) -> None:
    response = client.post(
        "/api/chat",
        json={
            "message": "hello",
            "attachments": [{"name": "../etc/passwd", "content": "x", "encoding": "text"}],
        },
        headers={"X-LLM-Provider": "google", "X-LLM-Model": "gemini-2.5-flash", "X-LLM-Key": "k"},
    )
    assert response.status_code == 422


def test_validate_requires_key(client: TestClient) -> None:
    response = client.post("/api/keys/validate")
    assert response.status_code == 401


def test_chat_streams_mocked_turn(client: TestClient) -> None:
    async def fake_turn(*_args, **_kwargs):
        yield {"type": "skill_loaded", "id": "1", "skill": "paper-search"}
        yield {"type": "text", "delta": "Here are papers."}

    with patch("app.routers.chat.factory.build_agent") as build, patch(
        "app.routers.chat.run_turn", fake_turn
    ):
        build.return_value = object()
        response = client.post(
            "/api/chat",
            json={"message": "find papers on RAG"},
            headers={"X-LLM-Provider": "google", "X-LLM-Model": "gemini-2.5-flash", "X-LLM-Key": "sk-test"},
        )
        assert response.status_code == 200
        text = response.text
        assert "event: skill_loaded" in text
        assert "Here are papers." in text
        assert "event: done" in text


def test_connectors(client: TestClient) -> None:
    response = client.get("/api/connectors")
    assert response.status_code == 200
    ids = [c["id"] for c in response.json()["connectors"]]
    assert ids == ["arxiv", "crossref", "openalex", "s2", "ncbi"]


def test_feedback_accepts_review(client: TestClient) -> None:
    response = client.post("/api/feedback", json={"kind": "up", "message": "Clear citations.", "source": "popup"})
    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_feedback_rejects_empty_kind(client: TestClient) -> None:
    response = client.post("/api/feedback", json={"kind": "maybe"})
    assert response.status_code == 422


def test_chat_accepts_deep_flag(client: TestClient) -> None:
    async def fake_turn(*_args, **_kwargs):
        yield {"type": "text", "delta": "Deep pass."}

    with patch("app.routers.chat.factory.build_agent") as build, patch(
        "app.routers.chat.run_turn", fake_turn
    ):
        build.return_value = object()
        response = client.post(
            "/api/chat",
            json={"message": "map this field", "deep": True},
            headers={"X-LLM-Provider": "google", "X-LLM-Model": "gemini-2.5-flash", "X-LLM-Key": "sk-test"},
        )
        assert response.status_code == 200
        assert "Deep pass." in response.text
        assert build.call_args.kwargs["deep"] is True


def test_catalog_matches_disk() -> None:
    catalog = load_catalog()
    assert len(catalog) == 59
    assert catalog["citation-verifier"].scripts
