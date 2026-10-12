"""Chat and key validation. The caller's API key arrives in a header and lives only for the request."""

from __future__ import annotations

import base64
import binascii
import json
import logging
import shutil
import tempfile
import time
from collections import defaultdict, deque
from pathlib import Path
from typing import Annotated, AsyncIterator, Literal

import httpx
import litellm
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, model_validator

from .. import config
from ..agent import factory
from ..agent.runner import run_turn
from ..agent.tools import safe_filename
from ..catalog import load_catalog
from ..errors import describe

router = APIRouter()
log = logging.getLogger("research_buddy")


class Credentials(BaseModel):
    provider: str
    model: str
    api_key: str
    s2_key: str | None = None
    ncbi_key: str | None = None

    def script_env(self) -> dict[str, str]:
        env = {"S2_API_KEY": self.s2_key, "NCBI_API_KEY": self.ncbi_key}
        return {k: v for k, v in env.items() if v}


def provider_key(
    provider: Annotated[str | None, Header(alias="X-LLM-Provider")] = None,
    api_key: Annotated[str | None, Header(alias="X-LLM-Key")] = None,
) -> tuple[config.Provider, str]:
    if not api_key or not api_key.strip():
        raise HTTPException(401, "Add your API key in Settings to start.")
    if provider not in config.PROVIDERS:
        raise HTTPException(400, "Unknown provider. Choose one in Settings.")
    return config.PROVIDERS[provider], api_key.strip()


def credentials(
    who: Annotated[tuple[config.Provider, str], Depends(provider_key)],
    model: Annotated[str | None, Header(alias="X-LLM-Model")] = None,
    s2_key: Annotated[str | None, Header(alias="X-S2-Key")] = None,
    ncbi_key: Annotated[str | None, Header(alias="X-NCBI-Key")] = None,
) -> Credentials:
    provider, api_key = who[0].id, who[1]
    model = (model or "").strip()
    if not model or len(model) > 200 or any(c.isspace() for c in model):
        raise HTTPException(400, "Choose a model in Settings.")
    return Credentials(provider=provider, model=model, api_key=api_key.strip(),
                       s2_key=(s2_key or "").strip() or None, ncbi_key=(ncbi_key or "").strip() or None)


class Turn(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1)


class Attachment(BaseModel):
    name: str
    content: str
    encoding: Literal["text", "base64"] = "text"


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=config.MAX_MESSAGE_CHARS)
    history: list[Turn] = Field(default_factory=list, max_length=config.MAX_HISTORY_TURNS)
    skill: str | None = None
    attachments: list[Attachment] = Field(default_factory=list, max_length=config.MAX_ATTACHMENTS)

    @model_validator(mode="after")
    def _check(self) -> "ChatRequest":
        if sum(len(t.content) for t in self.history) > config.MAX_HISTORY_CHARS:
            raise ValueError("the conversation is too long; start a new chat")
        if self.skill is not None and self.skill not in load_catalog():
            raise ValueError("unknown skill")
        for attachment in self.attachments:
            if not safe_filename(attachment.name):
                raise ValueError(f"attachment name {attachment.name!r} is not allowed; use letters, digits, dot, dash, underscore")
            if len(attachment.content) > config.MAX_ATTACHMENT_BYTES * 4 // 3 + 4:
                raise ValueError(f"attachment {attachment.name} is too large")
        return self


_hits: dict[str, deque[float]] = defaultdict(deque)


def rate_limit(request: Request) -> None:
    """Best-effort limit per client address. Each serverless instance counts on its own."""
    forwarded = request.headers.get("x-forwarded-for", "")
    client = forwarded.split(",")[0].strip() or (request.client.host if request.client else "unknown")
    now = time.monotonic()
    hits = _hits[client]
    while hits and now - hits[0] > config.RATE_LIMIT_WINDOW_SECONDS:
        hits.popleft()
    if len(hits) >= config.RATE_LIMIT_REQUESTS:
        raise HTTPException(429, "Too many requests. Wait a minute and try again.")
    hits.append(now)
    if len(_hits) > 5000:
        _hits.clear()


def _write_attachments(workdir: Path, attachments: list[Attachment]) -> list[str]:
    names = []
    for attachment in attachments:
        if attachment.encoding == "base64":
            try:
                data = base64.b64decode(attachment.content, validate=True)
            except (binascii.Error, ValueError) as exc:
                raise HTTPException(422, f"attachment {attachment.name} is not valid base64") from exc
        else:
            data = attachment.content.encode("utf-8")
        if len(data) > config.MAX_ATTACHMENT_BYTES:
            raise HTTPException(413, f"attachment {attachment.name} is too large")
        (workdir / attachment.name).write_bytes(data)
        names.append(attachment.name)
    return names


def sse(event: dict) -> str:
    return f"event: {event['type']}\ndata: {json.dumps(event, ensure_ascii=False)}\n\n"


@router.post("/chat", dependencies=[Depends(rate_limit)])
async def chat(body: ChatRequest, creds: Annotated[Credentials, Depends(credentials)]) -> StreamingResponse:
    workdir = Path(tempfile.mkdtemp(prefix="rb-"))
    try:
        attached = _write_attachments(workdir, body.attachments)
        agent = factory.build_agent(
            factory.build_model(creds.provider, creds.model, creds.api_key), workdir,
            pinned_skill=body.skill, attachments=attached, script_env=creds.script_env(),
            secrets=(creds.api_key, creds.s2_key or "", creds.ncbi_key or ""))
    except BaseException:
        shutil.rmtree(workdir, ignore_errors=True)
        raise

    async def stream() -> AsyncIterator[str]:
        failed = False
        try:
            async for event in run_turn(agent, [t.model_dump() for t in body.history], body.message):
                failed = failed or event["type"] == "error"
                yield sse(event)
            if not failed:
                yield sse({"type": "done"})
        except Exception as exc:  # the response has started, so report the failure in-band
            status, message = describe(exc, creds.api_key, creds.s2_key, creds.ncbi_key)
            log.warning("chat failed: %s (%s)", type(exc).__name__, status)
            if not failed:  # ADK may already have reported this failure as an event
                yield sse({"type": "error", "status": status, "message": message})
        finally:
            shutil.rmtree(workdir, ignore_errors=True)

    return StreamingResponse(stream(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache, no-transform", "X-Accel-Buffering": "no"})


@router.post("/keys/validate", dependencies=[Depends(rate_limit)])
async def validate_key(creds: Annotated[Credentials, Depends(credentials)]) -> dict:
    """Make one tiny call with the supplied key so the user learns now whether it works."""
    provider = config.PROVIDERS[creds.provider]
    try:
        await litellm.acompletion(
            model=provider.litellm_model(creds.model), api_key=creds.api_key,
            messages=[{"role": "user", "content": "Reply with the word ok."}],
            max_tokens=16, timeout=25, num_retries=0, drop_params=True)
    except Exception as exc:
        status, message = describe(exc, creds.api_key)
        return {"ok": False, "status": status, "message": message}
    return {"ok": True, "message": f"{provider.name} accepted the key for {creds.model}."}


_NOT_CHAT = ("embed", "whisper", "tts", "audio", "guard", "rerank", "moderation", "dall-e", "image", "imagen",
             "veo", "sora", "parse", "reward", "safety", "realtime", "transcribe", "aqa", "retriever", "clip")


@router.get("/models", dependencies=[Depends(rate_limit)])
async def list_models(who: Annotated[tuple[config.Provider, str], Depends(provider_key)]) -> dict:
    """Ask the provider which chat models this key can use, so the UI never offers a retired one."""
    provider, api_key = who
    headers = {"Authorization": f"Bearer {api_key}"}
    if provider.id == "google":
        headers = {"x-goog-api-key": api_key}
    elif provider.id == "anthropic":
        headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01"}
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(provider.models_url, headers=headers)
    except httpx.HTTPError:
        raise HTTPException(502, f"Could not reach {provider.name}.") from None
    if response.status_code in (400, 401, 403):
        raise HTTPException(401, f"{provider.name} rejected this API key.")
    if response.status_code != 200:
        raise HTTPException(502, f"{provider.name} returned an error ({response.status_code}).")

    data = response.json()
    if provider.id == "google":
        ids = [m["name"].removeprefix("models/") for m in data.get("models", [])
               if "generateContent" in m.get("supportedGenerationMethods", [])]
    elif provider.id == "openrouter":
        ids = [m["id"] for m in data.get("data", []) if "tools" in (m.get("supported_parameters") or [])]
    else:
        ids = [m["id"] for m in data.get("data", [])]
    return {"models": sorted(i for i in ids if not any(word in i.lower() for word in _NOT_CHAT))}
