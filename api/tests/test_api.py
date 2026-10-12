from __future__ import annotations

import asyncio
import logging

from app import config
from app.agent.tools import check_args, make_script_tools
from app.catalog import load_catalog
from app.errors import describe

from conftest import HEADERS, call, events, text


# ----------------------------------------------------------------------- catalog

def test_catalog_has_every_skill_in_twelve_stages():
    catalog = load_catalog()
    assert len(catalog) == 59
    assert {e.stage_index for e in catalog.values()} == set(range(1, 13))
    search = catalog["paper-search"]
    assert search.title == "Paper Search"
    assert search.scripts == ("search_papers.py",)
    assert "literature-search" in search.tags
    assert catalog["publication-figure-maker"].scripts == ()  # matplotlib script is blocked


def test_skills_endpoints(client):
    body = client.get("/api/skills").json()
    assert len(body["skills"]) == 59 and len(body["stages"]) == 12
    assert sum(s["count"] for s in body["stages"]) == 59
    assert "markdown" not in body["skills"][0]

    detail = client.get("/api/skills/citation-verifier").json()
    assert detail["markdown"].startswith("# Citation Verifier")
    assert client.get("/api/skills/nope").status_code == 404
    assert client.get("/api/health").json() == {"status": "ok", "skills": 59}
    assert {p["id"] for p in client.get("/api/providers").json()["providers"]} == set(config.PROVIDERS)


# ------------------------------------------------------------------ script tools

def test_check_args_rejects_paths_outside_the_working_folder():
    assert check_args(["retrieval augmented generation", "--limit", "10", "--out", "results.json"]) is None
    assert check_args(["refs.bib", "--tex=paper.tex"]) is None
    for bad in (["../secrets"], ["--out", "/etc/passwd"], ["--out=C:\\Windows\\x"], ["~/.ssh/id_rsa"],
                ["a/../../b"], ["\\\\server\\share"]):
        assert check_args(bad), bad


def test_run_script_runs_allowlisted_scripts_only(tmp_path):
    write_file, read_file, run_script = make_script_tools(tmp_path)

    result = asyncio.run(run_script("sample-size-power-calculator", "power_calc.py",
                                    ["ttest-ind", "--effect", "0.5", "--power", "0.8"]))
    assert result["status"] == "ok", result
    assert "64" in result["stdout"]  # the textbook answer: 64 per group

    assert asyncio.run(run_script("paper-search", "_scholarly_api.py", []))["status"] == "error"
    assert asyncio.run(run_script("experiment-logger", "log_run.py", []))["status"] == "error"
    assert asyncio.run(run_script("no-such-skill", "x.py", []))["status"] == "error"
    assert asyncio.run(run_script("paper-search", "../../../index.py", []))["status"] == "error"
    assert asyncio.run(run_script("paper-search", "search_papers.py", ["q", "--out", "../x"]))["status"] == "error"


def test_script_reads_files_written_to_the_working_folder(tmp_path):
    write_file, read_file, run_script = make_script_tools(tmp_path)
    assert write_file("../evil.csv", "x")["status"] == "error"
    assert write_file("results.csv", "Model,Accuracy\nA,0.91\nB,0.95\n")["status"] == "ok"

    result = asyncio.run(run_script("latex-table-generator", "csv_to_booktabs.py", ["results.csv"]))
    assert result["status"] == "ok", result
    assert "\\toprule" in result["stdout"] and "\\textbf{0.95}" in result["stdout"]

    assert read_file("results.csv")["content"].startswith("Model,Accuracy")
    assert read_file("missing.txt")["status"] == "error"


# --------------------------------------------------------------------------- chat

def test_chat_requires_credentials(client):
    assert client.post("/api/chat", json={"message": "hi"}).status_code == 401
    bad = {**HEADERS, "X-LLM-Provider": "nope"}
    assert client.post("/api/chat", json={"message": "hi"}, headers=bad).status_code == 400
    assert client.post("/api/keys/validate").status_code == 401
    assert client.get("/api/models").status_code == 401
    assert client.get("/api/models", headers=bad).status_code == 400


def test_models_are_listed_from_the_provider_and_filtered(client, monkeypatch):
    import httpx

    seen = {}

    async def fake_get(self, url, headers=None):
        seen.update(url=url, headers=headers)
        return httpx.Response(200, json={"data": [{"id": "chat-large"}, {"id": "text-embed-3"}, {"id": "chat-mini"}]})

    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get)
    response = client.get("/api/models", headers=HEADERS)
    assert response.json() == {"models": ["chat-large", "chat-mini"]}
    assert seen["url"] == "https://api.openai.com/v1/models"
    assert seen["headers"] == {"Authorization": "Bearer " + HEADERS["X-LLM-Key"]}

    async def refused(self, url, headers=None):
        return httpx.Response(401, json={"error": "bad key"})

    monkeypatch.setattr(httpx.AsyncClient, "get", refused)
    assert client.get("/api/models", headers=HEADERS).status_code == 401


def test_chat_validates_the_body(client, scripted):
    scripted(text("unused"))
    assert client.post("/api/chat", json={"message": ""}, headers=HEADERS).status_code == 422
    response = client.post("/api/chat", json={"message": "hi", "skill": "nope"}, headers=HEADERS)
    assert response.status_code == 422 and "unknown skill" in response.json()["message"]
    response = client.post("/api/chat", headers=HEADERS, json={
        "message": "hi", "attachments": [{"name": "../x.bib", "content": "a"}]})
    assert response.status_code == 422


def test_chat_streams_skill_loading_a_script_run_and_the_answer(client, scripted):
    model = scripted(
        call("load_skill", skill_name="sample-size-power-calculator"),
        call("run_script", skill_name="sample-size-power-calculator", script="power_calc.py",
             args=["ttest-ind", "--effect", "0.5", "--power", "0.8"]),
        text("You need 64 participants per group."),
    )
    response = client.post("/api/chat", headers=HEADERS, json={
        "message": "How many participants for d = 0.5?",
        "history": [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi, what are you studying?"}],
        "skill": "sample-size-power-calculator",
    })
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    stream = events(response)
    kinds = [e["type"] for e in stream]
    assert kinds == ["skill_loaded", "tool_call", "tool_result", "text", "done"], stream
    assert stream[0]["skill"] == "sample-size-power-calculator"
    assert stream[1]["name"] == "run_script" and stream[1]["args"]["script"] == "power_calc.py"
    assert stream[2]["ok"] is True and "64" in stream[2]["preview"]
    assert stream[3]["delta"] == "You need 64 participants per group."

    # The model saw the replayed history, the pinned skill, and the skill's instructions.
    first, last = model.requests[0], model.requests[-1]
    sent = [p.text for c in first.contents for p in c.parts if p.text]
    assert sent == ["Hello", "Hi, what are you studying?", "How many participants for d = 0.5?"]
    assert "chose the `sample-size-power-calculator` skill" in first.config.system_instruction
    assert {"list_skills", "load_skill", "load_skill_resource", "run_script", "write_file", "read_file"} \
        <= set(first.tools_dict)
    assert "power_calc.py" in str(last.contents)


def test_chat_passes_attachments_to_scripts(client, scripted):
    scripted(
        call("run_script", skill_name="latex-table-generator", script="csv_to_booktabs.py", args=["r.csv"]),
        text("done"),
    )
    response = client.post("/api/chat", headers=HEADERS, json={
        "message": "make a table", "attachments": [{"name": "r.csv", "content": "Model,Acc\nA,0.9\nB,0.8\n"}]})
    result = next(e for e in events(response) if e["type"] == "tool_result")
    assert result["ok"] and "\\toprule" in result["preview"]


def test_provider_errors_are_reported_in_band_without_the_key(client, scripted, caplog):
    key = HEADERS["X-LLM-Key"]

    class AuthenticationError(Exception):
        pass

    scripted(AuthenticationError(f"Incorrect API key provided: {key}"))
    with caplog.at_level(logging.DEBUG):
        response = client.post("/api/chat", json={"message": "hi"}, headers=HEADERS)
    stream = events(response)
    assert stream[-1]["type"] == "error" and stream[-1]["status"] == 401
    assert key not in response.text and key not in caplog.text

    status, message = describe(ValueError(f"boom {key}"), key)
    assert status == 500 and key not in message


def test_rate_limit(client, scripted, monkeypatch):
    monkeypatch.setattr(config, "RATE_LIMIT_REQUESTS", 2)
    for _ in range(2):
        scripted(text("ok"))
        assert client.post("/api/chat", json={"message": "hi"}, headers=HEADERS).status_code == 200
    assert client.post("/api/chat", json={"message": "hi"}, headers=HEADERS).status_code == 429
