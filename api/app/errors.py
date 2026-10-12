"""Turns provider failures into messages that are safe and useful to show in the browser."""

from __future__ import annotations

# LiteLLM exception class name -> (HTTP status, message). Matched by name so the
# module does not depend on which exception classes a LiteLLM version exports.
_KNOWN = {
    "AuthenticationError": (401, "The provider rejected this API key. Check the key and the provider in Settings."),
    "PermissionDeniedError": (403, "This API key is not allowed to use that model."),
    "NotFoundError": (404, "The provider does not know this model. Check the model name in Settings."),
    "RateLimitError": (429, "The provider's rate limit or quota was reached. Wait a moment, or check your plan."),
    "ContextWindowExceededError": (413, "This conversation is too long for the model. Start a new chat or use a model with a larger context window."),
    "ContentPolicyViolationError": (400, "The provider blocked this request under its content policy."),
    "BadRequestError": (400, "The provider rejected the request."),
    "UnsupportedParamsError": (400, "This model does not support tool calling, which Research Buddy needs. Choose another model."),
    "APIConnectionError": (502, "Could not reach the provider."),
    "ServiceUnavailableError": (503, "The provider is unavailable right now. Try again shortly."),
    "InternalServerError": (502, "The provider returned a server error. Try again shortly."),
    "APIError": (502, "The provider returned an error."),
    "Timeout": (504, "The provider took too long to respond."),
}
_DETAIL_FOR = {"APIError", "BadRequestError", "NotFoundError", "APIConnectionError", "PermissionDeniedError"}


class ProviderError(Exception):
    """A model call failed. Carries a message that is already safe to log and show."""

    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message


def redact(text: str, *secrets: str | None) -> str:
    for secret in secrets:
        if secret and len(secret) >= 4:
            text = text.replace(secret, "[redacted]")
    return text


def describe(exc: BaseException, *secrets: str | None) -> tuple[int, str]:
    """(status, message) for an exception raised while calling the model."""
    if isinstance(exc, ProviderError):
        return exc.status, exc.message
    for cls in type(exc).__mro__:
        if cls.__name__ in _KNOWN:
            status, message = _KNOWN[cls.__name__]
            if cls.__name__ in _DETAIL_FOR:
                detail = redact(str(exc), *secrets).strip().splitlines()
                if detail:
                    message += " Details: " + detail[0][:300]
            return status, message
    return 500, "Something went wrong while running the agent: " + redact(f"{type(exc).__name__}: {exc}", *secrets)[:300]
