"""Read-only catalog endpoints: skills, lifecycle stages, and LLM providers."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response

from ..catalog import load_catalog, stages
from ..config import PROVIDERS

router = APIRouter()
_CACHE = "public, max-age=300, s-maxage=3600, stale-while-revalidate=86400"


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "skills": len(load_catalog())}


@router.get("/skills")
def list_skills(response: Response) -> dict:
    response.headers["Cache-Control"] = _CACHE
    return {"stages": stages(), "skills": [entry.brief() for entry in load_catalog().values()]}


@router.get("/skills/{name}")
def get_skill(name: str, response: Response) -> dict:
    entry = load_catalog().get(name)
    if entry is None:
        raise HTTPException(404, "No such skill.")
    response.headers["Cache-Control"] = _CACHE
    return entry.detail()


@router.get("/providers")
def list_providers(response: Response) -> dict:
    response.headers["Cache-Control"] = _CACHE
    return {"providers": [{"id": p.id, "name": p.name, "key_hint": p.key_hint, "key_url": p.key_url} for p in PROVIDERS.values()]}
