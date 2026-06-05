from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Optional
from uuid import uuid4

IDEMPOTENCY_WINDOW_SECONDS = 300  # 5 minutes


@dataclass
class StoredUser:
    id: str
    email: str
    password_hash: str


class InMemoryUserStore:
    def __init__(self) -> None:
        self._users_by_email: Dict[str, StoredUser] = {}
        self._users_by_id: Dict[str, StoredUser] = {}

    def get_by_email(self, email: str) -> Optional[StoredUser]:
        return self._users_by_email.get(email.lower())

    def get_by_id(self, user_id: str) -> Optional[StoredUser]:
        return self._users_by_id.get(user_id)

    def create_user(self, email: str, password_hash: str) -> StoredUser:
        user = StoredUser(id=str(uuid4()), email=email.lower(), password_hash=password_hash)
        self._users_by_email[user.email] = user
        self._users_by_id[user.id] = user
        return user


@dataclass
class StoredInspection:
    id: str
    user_id: str
    mode: str
    status: str
    created_at: str


class InMemoryInspectionStore:
    def __init__(self) -> None:
        self._inspections: Dict[str, StoredInspection] = {}

    def create(self, user_id: str, mode: str, created_at: str) -> StoredInspection:
        inspection = StoredInspection(
            id=str(uuid4()),
            user_id=user_id,
            mode=mode,
            status="pending",
            created_at=created_at,
        )
        self._inspections[inspection.id] = inspection
        return inspection

    def get_by_id(self, inspection_id: str) -> Optional[StoredInspection]:
        return self._inspections.get(inspection_id)

    def find_recent(self, user_id: str, mode: str, now: datetime) -> Optional[StoredInspection]:
        """Return an existing pending inspection for user+mode within the idempotency window."""
        cutoff = now.timestamp() - IDEMPOTENCY_WINDOW_SECONDS
        for insp in self._inspections.values():
            if (
                insp.user_id == user_id
                and insp.mode == mode
                and insp.status == "pending"
                and datetime.fromisoformat(insp.created_at).timestamp() >= cutoff
            ):
                return insp
        return None


class InMemoryPaymentStore:
    """Minimal per-user payment status flag for gating osmosis inspections."""

    def __init__(self) -> None:
        self._valid_users: Dict[str, bool] = {}

    def set_payment_valid(self, user_id: str, valid: bool = True) -> None:
        self._valid_users[user_id] = valid

    def is_payment_valid(self, user_id: str) -> bool:
        return self._valid_users.get(user_id, False)


@dataclass
class QueuedJob:
    inspection_id: str
    user_id: str
    mode: str


class InMemoryJobQueue:
    """Minimal in-memory job queue for inspection processing."""

    def __init__(self) -> None:
        self._jobs: Dict[str, QueuedJob] = {}  # keyed by inspection_id

    def enqueue(self, inspection_id: str, user_id: str, mode: str) -> QueuedJob:
        """Enqueue a job. Idempotent: returns existing job if already enqueued."""
        if inspection_id in self._jobs:
            return self._jobs[inspection_id]
        job = QueuedJob(inspection_id=inspection_id, user_id=user_id, mode=mode)
        self._jobs[inspection_id] = job
        return job

    def get_by_inspection_id(self, inspection_id: str) -> Optional[QueuedJob]:
        return self._jobs.get(inspection_id)

    def pop_by_inspection_id(self, inspection_id: str) -> Optional[QueuedJob]:
        """Remove and return the job by inspection_id, consuming it."""
        return self._jobs.pop(inspection_id, None)



@dataclass
class StoredResult:
    inspection_id: str
    mode: str
    signal_detected: str
    confidence_level: str
    guidance: list
    model_version: str
    created_at: str


class InMemoryResultStore:
    """Minimal in-memory result store for completed inspection results."""

    def __init__(self) -> None:
        self._results: Dict[str, StoredResult] = {}  # keyed by inspection_id

    def save(self, result: StoredResult) -> StoredResult:
        self._results[result.inspection_id] = result
        return result

    def get_by_inspection_id(self, inspection_id: str) -> Optional[StoredResult]:
        return self._results.get(inspection_id)
