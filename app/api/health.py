from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict:
    """Liveness check. Returns {"status": "ok"} when the API process is up."""
    return {"status": "ok"}
