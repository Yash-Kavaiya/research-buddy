"""Turn provider and runtime failures into a status and a message that never contains secrets."""

from __future__ import annotations


class ProviderError(Exception):
    """A model-provider failure whose details have already been scrubbed."""

    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status
        self.message = message


def redact(text: str, *secrets: str | None) -> str:
    for secret in secrets:
        if secret:
            text = text.replace(secret, "…")
    return text


def describe(exc: BaseException, *secrets: str | None) -> tuple[int, str]:
    """Return (http_status, user_message) with API keys stripped out."""
    if isinstance(exc, ProviderError):
        return exc.status, redact(exc.message, *secrets)

    status = getattr(exc, "status_code", None) or getattr(exc, "status", None)
    try:
        status = int(status) if status is not None else None
    except (TypeError, ValueError):
        status = None

    raw = redact(str(exc), *secrets).strip() or type(exc).__name__
    # LiteLLM prefixes messages with "litellm.AuthenticationError: " and similar.
    if ": " in raw:
        head, tail = raw.split(": ", 1)
        if head.lower().startswith("litellm") or "error" in head.lower():
            raw = tail
    line = raw.splitlines()[0].strip()[:400]

    if status in (401, 403):
        return 401, "The provider rejected the API key. Check it in Settings."
    if status == 404:
        return 404, "That model is not available on this provider. Pick another in Settings."
    if status == 429:
        return 429, "The provider rate-limited this key. Wait a minute and try again."
    if status == 400:
        return 400, line or "The provider rejected the request."
    if status and 400 <= status < 500:
        return status, line or "The provider rejected the request."
    if "api key" in line.lower() or "authentication" in line.lower() or "unauthorized" in line.lower():
        return 401, "The provider rejected the API key. Check it in Settings."
    if "rate" in line.lower() and "limit" in line.lower():
        return 429, "The provider rate-limited this key. Wait a minute and try again."
    return 502, line or "The model provider failed. Try again, or pick another model."
