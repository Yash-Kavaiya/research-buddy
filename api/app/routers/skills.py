"""Skill catalog and provider list. These endpoints do not need an API key."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .. import config
from ..catalog import load_catalog, skill_detail, skill_summary, stages_payload

router = APIRouter()


@router.get("/health")
async def health() -> dict:
    return {"ok": True, "skills": len(load_catalog())}


@router.get("/skills")
async def list_skills() -> dict:
    catalog = load_catalog()
    return {
        "stages": stages_payload(),
        "skills": [skill_summary(entry) for entry in catalog.values()],
    }


@router.get("/skills/{name}")
async def get_skill(name: str) -> dict:
    entry = load_catalog().get(name)
    if entry is None:
        raise HTTPException(404, "Unknown skill.")
    return skill_detail(entry)


@router.get("/providers")
async def providers() -> dict:
    return {
        "providers": [
            {
                "id": p.id,
                "name": p.name,
                "keyHint": p.key_hint,
                "keyUrl": p.key_url,
                "models": p.models,
            }
            for p in config.PROVIDERS.values()
        ]
    }
