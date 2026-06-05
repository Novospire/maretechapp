from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core.store import InMemoryInspectionStore, InMemoryJobQueue, InMemoryPaymentStore, InMemoryResultStore, StoredUser
from app.dependencies import get_current_user, get_inspection_store, get_payment_store, get_job_queue, get_result_store
from app.schemas import InspectionCreate, InspectionCreated, CompleteResponse, InspectionStatusResponse, InspectionResultResponse


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


@router.post("/{inspection_id}/complete", response_model=CompleteResponse)
async def complete_upload(
    inspection_id: str,
    current_user: StoredUser = Depends(get_current_user),
    inspection_store: InMemoryInspectionStore = Depends(get_inspection_store),
    job_queue: InMemoryJobQueue = Depends(get_job_queue),
):
    inspection = inspection_store.get_by_id(inspection_id)
    if not inspection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inspection not found")

    if inspection.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Mark upload complete internally by updating status
    inspection.status = "queued"

    # Enqueue job
    job_queue.enqueue(inspection_id=inspection.id, user_id=current_user.id, mode=inspection.mode)

    return CompleteResponse(status="queued")


@router.get("/{inspection_id}", response_model=InspectionStatusResponse)
async def get_inspection_status(
    inspection_id: str,
    current_user: StoredUser = Depends(get_current_user),
    inspection_store: InMemoryInspectionStore = Depends(get_inspection_store),
):
    inspection = inspection_store.get_by_id(inspection_id)
    if not inspection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inspection not found")

    if inspection.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Map internal status to API Spec status
    public_status = inspection.status
    if public_status == "queued":
        public_status = "pending"

    return InspectionStatusResponse(
        inspection_id=inspection.id,
        status=public_status,
    )


@router.get("/{inspection_id}/result", response_model=InspectionResultResponse)
async def get_inspection_result(
    inspection_id: str,
    current_user: StoredUser = Depends(get_current_user),
    inspection_store: InMemoryInspectionStore = Depends(get_inspection_store),
    result_store: InMemoryResultStore = Depends(get_result_store),
):
    inspection = inspection_store.get_by_id(inspection_id)
    if not inspection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inspection not found")

    if inspection.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    if inspection.status != "completed":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Inspection result not available")

    result = result_store.get_by_inspection_id(inspection_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Result not found")

    return InspectionResultResponse(
        inspection_id=result.inspection_id,
        mode=result.mode,
        signal_detected=result.signal_detected,
        confidence_level=result.confidence_level,
        guidance=result.guidance,
        model_version=result.model_version,
        created_at=result.created_at,
    )
