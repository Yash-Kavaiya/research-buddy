"""Connectors catalog and on-device feedback. Neither endpoint stores a key or a review."""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()

CONNECTORS = [
    {
        "id": "arxiv",
        "name": "arXiv",
        "detail": "Built in. Paper search uses it with no key.",
        "kind": "builtin",
    },
    {
        "id": "crossref",
        "name": "Crossref",
        "detail": "Built in. Citation checks use it with no key.",
        "kind": "builtin",
    },
    {
        "id": "openalex",
        "name": "OpenAlex",
        "detail": "Optional contact email. It raises the polite rate limit; search works without it.",
        "kind": "email",
        "header": "X-OpenAlex-Email",
    },
    {
        "id": "s2",
        "name": "Semantic Scholar",
        "detail": "Optional API key for higher rate limits on literature search.",
        "kind": "key",
        "header": "X-S2-Key",
        "keyUrl": "https://www.semanticscholar.org/product/api#api-key-form",
    },
    {
        "id": "ncbi",
        "name": "PubMed / NCBI",
        "detail": "Optional API key for higher PubMed rate limits.",
        "kind": "key",
        "header": "X-NCBI-Key",
        "keyUrl": "https://www.ncbi.nlm.nih.gov/account/settings/",
    },
]


class FeedbackIn(BaseModel):
    kind: Literal["up", "down", "review"]
    message: str = Field(default="", max_length=4000)
    source: Literal["popup", "message", "support"] = "support"


@router.get("/connectors")
async def connectors() -> dict:
    return {"connectors": CONNECTORS}


@router.post("/feedback")
async def feedback(body: FeedbackIn) -> dict:
    """Accept a review. The browser keeps the copy; the server does not store it."""
    return {
        "ok": True,
        "message": "Review noted on this device. Nothing was stored on the server.",
    }
