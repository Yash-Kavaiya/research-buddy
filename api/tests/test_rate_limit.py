from __future__ import annotations

import pytest
from fastapi import HTTPException
from starlette.requests import Request

from app import config
from app.routers import chat


def _request(headers: dict[str, str] | None = None, host: str = "203.0.113.9") -> Request:
    raw = [(k.lower().encode(), v.encode()) for k, v in (headers or {}).items()]
    return Request({"type": "http", "headers": raw, "client": (host, 1234)})


@pytest.fixture(autouse=True)
def _reset(monkeypatch):
    chat._hits.clear()
    monkeypatch.setattr(config, "RATE_LIMIT_REQUESTS", 3)
    yield
    chat._hits.clear()


def test_spoofed_forwarded_for_does_not_bypass_the_limit() -> None:
    for i in range(3):
        chat.rate_limit(_request({"X-Forwarded-For": f"10.0.0.{i}"}))
    with pytest.raises(HTTPException) as exc:
        chat.rate_limit(_request({"X-Forwarded-For": "10.0.0.99"}))
    assert exc.value.status_code == 429


def test_x_real_ip_identifies_the_client() -> None:
    for _ in range(3):
        chat.rate_limit(_request({"X-Real-IP": "198.51.100.1"}))
    with pytest.raises(HTTPException):
        chat.rate_limit(_request({"X-Real-IP": "198.51.100.1"}))
    chat.rate_limit(_request({"X-Real-IP": "198.51.100.2"}))


def test_flooding_new_clients_does_not_reset_existing_counters(monkeypatch) -> None:
    monkeypatch.setattr(chat, "_MAX_TRACKED_CLIENTS", 10)
    for _ in range(3):
        chat.rate_limit(_request({"X-Real-IP": "198.51.100.1"}))
    for i in range(5):
        chat.rate_limit(_request({"X-Real-IP": f"192.0.2.{i}"}))
    with pytest.raises(HTTPException):
        chat.rate_limit(_request({"X-Real-IP": "198.51.100.1"}))
    for i in range(50):
        chat.rate_limit(_request({"X-Real-IP": f"192.0.2.{100 + i}"}))
    assert len(chat._hits) <= 10
