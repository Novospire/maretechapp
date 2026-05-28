from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core.store import InMemoryInspectionStore, InMemoryPaymentStore, StoredUser
from app.dependencies import get_current_user, get_inspection_store, get_payment_store
from app.schemas import InspectionCreate, InspectionCreated


router = APIRouter(prefix="/inspections", tags=["inspections"])

UPLOAD_URL_COUNT = 2
UPLOAD_EXPIRY_MINUTES = 30


def _generate_mock_upload_urls(inspection_id: str, count: int) -> list[str]:
    """Return deterministic mock presigned upload URLs."""
    return [
        f"https://storage.example.com/{inspection_id}/upload_{i}"
        for i in range(count)
    ]


def _build_response(inspection_id: str, created_at: str) -> InspectionCreated:
    upload_urls = _generate_mock_upload_urls(inspection_id, UPLOAD_URL_COUNT)
    created_dt = datetime.fromisoformat(created_at)
    expires_at = (created_dt + timedelta(minutes=UPLOAD_EXPIRY_MINUTES)).isoformat()
    return InspectionCreated(
        inspection_id=inspection_id,
        upload_urls=upload_urls,
        expires_at=expires_at,
    )


@router.post("", response_model=InspectionCreated, status_code=status.HTTP_201_CREATED)
async def create_inspection(
    payload: InspectionCreate,
    response: Response,
    current_user: StoredUser = Depends(get_current_user),
    inspection_store: InMemoryInspectionStore = Depends(get_inspection_store),
    payment_store: InMemoryPaymentStore = Depends(get_payment_store),
):
    # Osmosis requires valid payment
    if payload.mode == "osmosis" and not payment_store.is_payment_valid(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Osmosis inspection requires valid payment",
        )

    now = datetime.now(timezone.utc)

    # Idempotency: return existing inspection if one matches user+mode within window
    existing = inspection_store.find_recent(current_user.id, payload.mode, now)
    if existing:
        response.status_code = status.HTTP_200_OK
        return _build_response(existing.id, existing.created_at)

    inspection = inspection_store.create(
        user_id=current_user.id,
        mode=payload.mode,
        created_at=now.isoformat(),
    )

    return _build_response(inspection.id, inspection.created_at)
