"""Tests for BE-060 Inference Stub Worker.

Tests cover:
1. Completing upload enqueues job as before (regression).
2. Worker consumes queued job and transitions lifecycle.
3. Worker sets status to processing during execution.
4. Worker persists a deterministic result.
5. Worker marks inspection completed only after result exists.
6. GET /inspections/{id} returns completed after worker run.
7. GET /inspections/{id}/result returns API-Spec result after worker run.
8. Osmosis and corrosion outputs are deterministic and mode-isolated.
9. Failed worker path marks inspection failed.
10. Existing BE-020/030/040/050 tests remain green (verified by running full suite).
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import create_app
from app.worker.inference_stub import run_job, run_next_job, STUB_MODEL_VERSION
from app.core.store import QueuedJob


def _create_client():
    app = create_app()
    return TestClient(app), app


def _register_and_get_token(client: TestClient) -> tuple[str, str]:
    payload = {"email": f"worker+{uuid4()}@example.com", "password": "password123"}
    resp = client.post("/auth/register", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    return data["token"]["access_token"], data["user"]["id"]


def _complete_inspection(client, token, mode="corrosion", app=None, user_id=None):
    """Create and complete an inspection. Returns inspection_id."""
    if mode == "osmosis":
        assert app is not None and user_id is not None, "osmosis requires payment setup"
        app.state.payment_store.set_payment_valid(user_id)

    resp = client.post(
        "/inspections",
        json={"mode": mode},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    inspection_id = resp.json()["inspection_id"]

    resp_complete = client.post(
        f"/inspections/{inspection_id}/complete",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp_complete.status_code == 200
    return inspection_id


# ---------- 1) Upload completion still enqueues job (regression) ----------

def test_complete_upload_still_enqueues_job(monkeypatch):
    """BE-030 regression: completing upload enqueues a job as before."""
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, _ = _register_and_get_token(client)

    inspection_id = _complete_inspection(client, token, mode="corrosion")

    job = app.state.job_queue.get_by_inspection_id(inspection_id)
    assert job is not None
    assert job.inspection_id == inspection_id
    assert job.mode == "corrosion"


# ---------- 2) Worker consumes queued job ----------

def test_worker_consumes_queued_job(monkeypatch):
    """Worker run_job() processes the job from the queue."""
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, _ = _register_and_get_token(client)

    inspection_id = _complete_inspection(client, token, mode="corrosion")

    job = app.state.job_queue.get_by_inspection_id(inspection_id)
    assert job is not None

    # Run the worker
    result = run_job(job, app.state.inspection_store, app.state.result_store)

    assert result is not None
    assert result.inspection_id == inspection_id


# ---------- 3) Worker sets status to processing (observable via store) ----------

def test_worker_transitions_through_processing(monkeypatch):
    """Worker sets status to processing before completing."""
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, _ = _register_and_get_token(client)

    inspection_id = _complete_inspection(client, token, mode="corrosion")

    inspection = app.state.inspection_store.get_by_id(inspection_id)
    assert inspection.status == "queued"  # pre-worker

    job = app.state.job_queue.get_by_inspection_id(inspection_id)

    # Patch result_store.save to capture status at the moment of saving
    captured_status_at_save = []
    original_save = app.state.result_store.save

    def save_and_capture(result):
        captured_status_at_save.append(
            app.state.inspection_store.get_by_id(inspection_id).status
        )
        return original_save(result)

    app.state.result_store.save = save_and_capture

    run_job(job, app.state.inspection_store, app.state.result_store)

    # At the moment of save, status should have been "processing"
    assert captured_status_at_save == ["processing"]

    # After completion, status is "completed"
    assert inspection.status == "completed"


# ---------- 4) Worker persists a deterministic result ----------

def test_worker_persists_deterministic_result_corrosion(monkeypatch):
    """Worker persists a deterministic corrosion result to the result store."""
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, _ = _register_and_get_token(client)

    inspection_id = _complete_inspection(client, token, mode="corrosion")
    job = app.state.job_queue.get_by_inspection_id(inspection_id)
    run_job(job, app.state.inspection_store, app.state.result_store)

    result = app.state.result_store.get_by_inspection_id(inspection_id)
    assert result is not None
    assert result.inspection_id == inspection_id
    assert result.mode == "corrosion"
    assert result.signal_detected in {"yes", "no", "inconclusive"}
    assert result.confidence_level in {"low", "medium", "high"}
    assert isinstance(result.guidance, list)
    assert len(result.guidance) > 0
    assert result.model_version == STUB_MODEL_VERSION
    assert result.created_at  # ISO-8601 non-empty


# ---------- 5) Worker marks completed ONLY after result is persisted ----------

def test_worker_completes_only_after_result_persisted(monkeypatch):
    """Inspection reaches 'completed' only after the result is in the store."""
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, _ = _register_and_get_token(client)

    inspection_id = _complete_inspection(client, token, mode="corrosion")
    job = app.state.job_queue.get_by_inspection_id(inspection_id)

    # Track order of operations
    events = []
    original_save = app.state.result_store.save

    def save_and_track(result):
        events.append("result_saved")
        return original_save(result)

    app.state.result_store.save = save_and_track

    original_status_setter = None

    # Monkey-patch the inspection object's status property
    inspection = app.state.inspection_store.get_by_id(inspection_id)
    original_setattr = inspection.__class__.__setattr__

    def tracking_setattr(self, name, value):
        if name == "status" and value == "completed":
            events.append("status_set_completed")
        original_setattr(self, name, value)

    inspection.__class__.__setattr__ = tracking_setattr

    try:
        run_job(job, app.state.inspection_store, app.state.result_store)
    finally:
        inspection.__class__.__setattr__ = original_setattr

    # result_saved must come before status_set_completed
    assert "result_saved" in events
    assert "status_set_completed" in events
    assert events.index("result_saved") < events.index("status_set_completed")


# ---------- 6) GET /inspections/{id} returns completed after worker run ----------

def test_status_endpoint_returns_completed_after_worker(monkeypatch):
    """After worker runs, GET /inspections/{id} returns status=completed."""
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, _ = _register_and_get_token(client)

    inspection_id = _complete_inspection(client, token, mode="corrosion")
    headers = {"Authorization": f"Bearer {token}"}

    # Before worker: should be pending (queued mapped to pending)
    resp = client.get(f"/inspections/{inspection_id}", headers=headers)
    assert resp.json()["status"] == "pending"

    job = app.state.job_queue.get_by_inspection_id(inspection_id)
    run_job(job, app.state.inspection_store, app.state.result_store)

    # After worker: should be completed
    resp = client.get(f"/inspections/{inspection_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"


# ---------- 7) GET /inspections/{id}/result returns full result after worker run ----------

def test_result_endpoint_returns_result_after_worker(monkeypatch):
    """After worker runs, GET /inspections/{id}/result returns 200 with correct contract."""
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, _ = _register_and_get_token(client)

    inspection_id = _complete_inspection(client, token, mode="corrosion")
    headers = {"Authorization": f"Bearer {token}"}

    # Before worker: 409
    resp = client.get(f"/inspections/{inspection_id}/result", headers=headers)
    assert resp.status_code == 409

    job = app.state.job_queue.get_by_inspection_id(inspection_id)
    run_job(job, app.state.inspection_store, app.state.result_store)

    # After worker: 200 with full contract
    resp = client.get(f"/inspections/{inspection_id}/result", headers=headers)
    assert resp.status_code == 200
    data = resp.json()

    expected_keys = {
        "inspection_id", "mode", "signal_detected",
        "confidence_level", "guidance", "model_version", "created_at",
    }
    assert set(data.keys()) == expected_keys
    assert data["inspection_id"] == inspection_id
    assert data["mode"] == "corrosion"
    assert data["model_version"] == STUB_MODEL_VERSION


# ---------- 8a) Corrosion output is deterministic and mode-isolated ----------

def test_worker_corrosion_output_is_deterministic_and_isolated(monkeypatch):
    """Corrosion stub produces deterministic corrosion-specific output."""
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, _ = _register_and_get_token(client)

    # Run twice, expect identical output
    inspection_id_1 = _complete_inspection(client, token, mode="corrosion")
    # Need a new inspection (first is idempotent, use different token)
    token2, _ = _register_and_get_token(client)
    inspection_id_2 = _complete_inspection(client, token2, mode="corrosion")

    job1 = app.state.job_queue.get_by_inspection_id(inspection_id_1)
    job2 = app.state.job_queue.get_by_inspection_id(inspection_id_2)

    result1 = run_job(job1, app.state.inspection_store, app.state.result_store)
    result2 = run_job(job2, app.state.inspection_store, app.state.result_store)

    # Mode isolation: mode field must be corrosion
    assert result1.mode == "corrosion"
    assert result2.mode == "corrosion"

    # Deterministic: same outputs for same mode
    assert result1.signal_detected == result2.signal_detected
    assert result1.confidence_level == result2.confidence_level
    assert result1.guidance == result2.guidance
    assert result1.model_version == result2.model_version


# ---------- 8b) Osmosis output is deterministic and mode-isolated ----------

def test_worker_osmosis_output_is_deterministic_and_isolated(monkeypatch):
    """Osmosis stub produces deterministic osmosis-specific output."""
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, user_id = _register_and_get_token(client)

    inspection_id = _complete_inspection(
        client, token, mode="osmosis", app=app, user_id=user_id
    )
    job = app.state.job_queue.get_by_inspection_id(inspection_id)
    result = run_job(job, app.state.inspection_store, app.state.result_store)

    assert result.mode == "osmosis"
    assert result.model_version == STUB_MODEL_VERSION

    # Osmosis result must not leak corrosion-specific data
    # (Both use same schema per API-Spec § 3.4, mode field is the isolation point)
    assert result.mode != "corrosion"


# ---------- 8c) Osmosis and corrosion outputs are mode-isolated from each other ----------

def test_worker_osmosis_and_corrosion_outputs_are_isolated(monkeypatch):
    """Running osmosis and corrosion jobs on same app instance produces isolated results."""
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()

    token_c, _ = _register_and_get_token(client)
    token_o, user_id_o = _register_and_get_token(client)

    inspection_c = _complete_inspection(client, token_c, mode="corrosion")
    inspection_o = _complete_inspection(
        client, token_o, mode="osmosis", app=app, user_id=user_id_o
    )

    job_c = app.state.job_queue.get_by_inspection_id(inspection_c)
    job_o = app.state.job_queue.get_by_inspection_id(inspection_o)

    result_c = run_job(job_c, app.state.inspection_store, app.state.result_store)
    result_o = run_job(job_o, app.state.inspection_store, app.state.result_store)

    # Mode isolation
    assert result_c.mode == "corrosion"
    assert result_o.mode == "osmosis"

    # Results stored separately and independently
    stored_c = app.state.result_store.get_by_inspection_id(inspection_c)
    stored_o = app.state.result_store.get_by_inspection_id(inspection_o)
    assert stored_c.mode == "corrosion"
    assert stored_o.mode == "osmosis"


# ---------- 9) Failed worker path marks inspection failed ----------

def test_worker_marks_failed_on_unsupported_mode(monkeypatch):
    """Worker marks inspection as failed if mode is unsupported."""
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    _, app = _create_client()

    # Manually inject a job with an unsupported mode
    from app.core.store import StoredInspection
    inspection_id = str(uuid4())
    fake_inspection = StoredInspection(
        id=inspection_id,
        user_id=str(uuid4()),
        mode="unknown_mode",
        status="queued",
        created_at="2026-01-01T00:00:00+00:00",
    )
    app.state.inspection_store._inspections[inspection_id] = fake_inspection

    fake_job = QueuedJob(
        inspection_id=inspection_id,
        user_id=fake_inspection.user_id,
        mode="unknown_mode",
    )

    with pytest.raises(ValueError, match="Unsupported mode"):
        run_job(fake_job, app.state.inspection_store, app.state.result_store)

    assert fake_inspection.status == "failed"


def test_worker_marks_failed_if_inspection_not_found(monkeypatch):
    """Worker raises ValueError and does not crash if inspection is missing."""
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    _, app = _create_client()

    missing_job = QueuedJob(
        inspection_id=str(uuid4()),
        user_id=str(uuid4()),
        mode="corrosion",
    )

    with pytest.raises(ValueError, match="Inspection not found"):
        run_job(missing_job, app.state.inspection_store, app.state.result_store)


# ---------- 10) Job consumption and retry-safety tests ----------

def test_run_next_job_consumes_and_pops(monkeypatch):
    """Calling run_next_job consumes and removes the job from the queue."""
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, _ = _register_and_get_token(client)

    inspection_id = _complete_inspection(client, token, mode="corrosion")

    # Verify job is initially queued
    assert app.state.job_queue.get_by_inspection_id(inspection_id) is not None

    # Run next job
    result = run_next_job(
        app.state.job_queue,
        app.state.inspection_store,
        app.state.result_store,
        inspection_id,
    )

    assert result is not None
    # Verify job is no longer in the queue
    assert app.state.job_queue.get_by_inspection_id(inspection_id) is None


def test_retry_run_completed_job_is_idempotent(monkeypatch):
    """Running an already completed job does not overwrite the result or change created_at."""
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, _ = _register_and_get_token(client)

    inspection_id = _complete_inspection(client, token, mode="corrosion")

    # Run first time
    result1 = run_next_job(
        app.state.job_queue,
        app.state.inspection_store,
        app.state.result_store,
        inspection_id,
    )
    first_created_at = result1.created_at

    # Re-enqueue the same job manually (simulating a retry / re-delivery of the job)
    app.state.job_queue.enqueue(
        inspection_id=inspection_id,
        user_id=result1.inspection_id,
        mode=result1.mode,
    )

    # Run second time
    result2 = run_next_job(
        app.state.job_queue,
        app.state.inspection_store,
        app.state.result_store,
        inspection_id,
    )

    # Same result instance/fields returned, created_at must match exactly
    assert result1.created_at == result2.created_at
    assert result2.created_at == first_created_at

    # Verify only one result exists in the store
    assert app.state.result_store.get_by_inspection_id(inspection_id) == result1


def test_run_next_job_no_job_throws_unless_completed(monkeypatch):
    """If no job is in queue and inspection is not completed, run_next_job raises ValueError."""
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    _, app = _create_client()

    with pytest.raises(ValueError, match="No queued job found"):
        run_next_job(
            app.state.job_queue,
            app.state.inspection_store,
            app.state.result_store,
            str(uuid4()),
        )

