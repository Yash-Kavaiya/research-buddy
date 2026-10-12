"""Runs one chat turn through ADK and translates its events into the app's stream events."""

from __future__ import annotations

import json
from typing import Any, AsyncIterator

from google.adk.agents import LlmAgent
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.events import Event
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from .. import config

APP_NAME = "research-buddy"
USER_ID = "browser"
_PREVIEW_CHARS = 4000


def _preview(value: Any) -> str:
    """A short, readable rendering of a tool result for the activity panel."""
    if isinstance(value, dict):
        for key in ("stdout", "content", "error", "result"):
            if isinstance(value.get(key), str) and value[key].strip():
                text = value[key]
                if key == "stdout" and value.get("stderr"):
                    text += "\n" + value["stderr"]
                return text[:_PREVIEW_CHARS]
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, default=str)
    return text[:_PREVIEW_CHARS]


def _ok(value: Any) -> bool:
    if isinstance(value, dict):
        return value.get("status") != "error" and "error" not in value
    return True


async def run_turn(agent: LlmAgent, history: list[dict], message: str) -> AsyncIterator[dict]:
    """Yield {'type': ..., ...} events for one user message.

    The server keeps no state between requests, so the conversation so far is replayed
    into a fresh in-memory session before the new message runs.
    """
    sessions = InMemorySessionService()
    session = await sessions.create_session(app_name=APP_NAME, user_id=USER_ID)
    for turn in history:
        is_user = turn["role"] == "user"
        await sessions.append_event(session, Event(
            author="user" if is_user else agent.name,
            content=types.Content(role="user" if is_user else "model", parts=[types.Part(text=turn["content"])]),
        ))

    runner = Runner(agent=agent, app_name=APP_NAME, session_service=sessions)
    run_config = RunConfig(streaming_mode=StreamingMode.SSE, max_llm_calls=config.MAX_LLM_CALLS)
    new_message = types.Content(role="user", parts=[types.Part(text=message)])

    soft_error: str | None = None
    streamed = False  # whether partial text was already sent for the model response in progress
    async for event in runner.run_async(user_id=USER_ID, session_id=session.id, new_message=new_message,
                                        run_config=run_config):
        if event.error_message:
            # Usually followed by the exception itself, which the caller reports with a status.
            soft_error = event.error_message
        parts = (event.content.parts if event.content else None) or []
        for part in parts:
            if part.text and not part.thought:
                if event.partial:
                    streamed = True
                    yield {"type": "text", "delta": part.text}
                elif not streamed:
                    yield {"type": "text", "delta": part.text}
            elif part.function_call and not event.partial:
                call = part.function_call
                args = dict(call.args or {})
                if call.name == "load_skill":
                    yield {"type": "skill_loaded", "id": call.id, "skill": args.get("skill_name") or args.get("name")}
                else:
                    yield {"type": "tool_call", "id": call.id, "name": call.name, "args": args}
            elif part.function_response:
                response = part.function_response
                if response.name != "load_skill":
                    yield {"type": "tool_result", "id": response.id, "name": response.name,
                           "ok": _ok(response.response), "preview": _preview(response.response)}
        if not event.partial:
            streamed = False
    if soft_error:
        yield {"type": "error", "message": soft_error}
