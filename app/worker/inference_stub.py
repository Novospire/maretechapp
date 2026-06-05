"""BE-060 — Inference Stub Worker (MVP).

This module provides run_job(), a synchronous function that consumes a
single queued job, transitions the inspection lifecycle, produces a
deterministic mocked result per mode, and persists it to the result store.

Design constraints (per Backend-Tickets.md + Agent-Operating-Protocol.md):
- AI inference is NEVER blocking a request thread.
  run_job() is called OUTSIDE the HTTP request/response cycle (e.g. from
  tests, a background task runner, or a future Celery task).
- Mode isolation: osmosis result payload must not contain corrosion fields
  and vice versa. Both share the same API-Spec § 3.4 contract but the
  `mode` field always reflects the originating inspection mode.
- Output language remains probabilistic: signal_detected, confidence_level,
  guidance — never definitive diagnosis language.
- Does not produce real AI inference; outputs are deterministic stubs.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone

from app.core.store import (
    InMemoryInspectionStore,
    InMemoryResultStore,
    QueuedJob,
    StoredResult,
)

logger = logging.getLogger("maretech.worker")

# Stub model version tag stored with every result.
STUB_MODEL_VERSION = "stub-v0.1.0"

# Deterministic mocked outputs per mode.
# Values are intentionally probabilistic (signal / risk / confidence language).
_MOCK_OUTPUTS: dict[str, dict] = {
    "osmosis": {
        "signal_detected": "yes",
        "confidence_level": "medium",
        "guidance": ["monitor", "recheck_later"],
    },
    "corrosion": {
        "signal_detected": "yes",
        "confidence_level": "low",
        "guidance": ["monitor"],
    },
}


def run_job(
    job: QueuedJob,
    inspection_store: InMemoryInspectionStore,
    result_store: InMemoryResultStore,
) -> StoredResult:
    """Process a single queued inference job.

    Lifecycle:
        queued  ->  processing  ->  completed   (happy path)
                                ->  failed      (on unhandled exception)

    Lifecycle integrity: inspection is only marked `completed` AFTER the
    result has been successfully persisted to result_store.

    Args:
        job: The queued job to process.
        inspection_store: The inspection store holding the lifecycle record.
        result_store: The result store where the output is persisted.

    Returns:
        The persisted StoredResult.

    Raises:
        ValueError: If the inspection is not found or mode is unsupported.
    """
    inspection = inspection_store.get_by_id(job.inspection_id)
    if inspection is None:
        raise ValueError(f"Inspection not found: {job.inspection_id}")

    mode = job.mode
    if mode not in _MOCK_OUTPUTS:
        inspection.status = "failed"
        raise ValueError(f"Unsupported mode: {mode}")

    logger.info("Worker: starting job inspection_id=%s mode=%s", job.inspection_id, mode)

    # Transition to processing
    inspection.status = "processing"

    try:
        outputs = _MOCK_OUTPUTS[mode]
        now = datetime.now(timezone.utc).isoformat()

        result = StoredResult(
            inspection_id=job.inspection_id,
            mode=mode,
            signal_detected=outputs["signal_detected"],
            confidence_level=outputs["confidence_level"],
            guidance=list(outputs["guidance"]),
            model_version=STUB_MODEL_VERSION,
            created_at=now,
        )

        # Persist result BEFORE marking completed (lifecycle integrity).
        result_store.save(result)

        # Only mark completed after successful persistence.
        inspection.status = "completed"

        logger.info(
            "Worker: completed job inspection_id=%s mode=%s signal=%s confidence=%s",
            job.inspection_id,
            mode,
            result.signal_detected,
            result.confidence_level,
        )

        return result

    except Exception:
        inspection.status = "failed"
        logger.exception("Worker: job failed inspection_id=%s", job.inspection_id)
        raise
