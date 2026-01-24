from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.dependencies import get_current_user


router = APIRouter(prefix="/capture-policy", tags=["capture-policy"])


@router.get("/{mode}")
async def get_capture_policy(mode: str, current_user=Depends(get_current_user)):
    if mode == "corrosion":
        return {
            "mode": "corrosion",
            "free_points": 5,
            "max_points": 10,
            "angles_per_point": 3,
        }
    if mode == "osmosis":
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error_code": "POLICY_NOT_DEFINED",
                "detail": "Osmosis capture policy not defined yet",
            },
        )
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid mode")
