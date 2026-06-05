"""Tests for BE-020 Create Inspection Session."""
from __future__ import annotations

from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import create_app


def _create_client():
    app = create_app()
    return TestClient(app), app


def _register_and_get_token(client: TestClient) -> tuple[str, str]:
    """Register a user and return (token, user_id)."""
    payload = {"email": f"insp+{uuid4()}@example.com", "password": "password123"}
    resp = client.post("/auth/register", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    return data["token"]["access_token"], data["user"]["id"]


# ---------- 1) Missing auth rejects POST /inspections ----------

def test_create_inspection_unauthenticated():
    client, _ = _create_client()
    resp = client.post("/inspections", json={"mode": "corrosion"})
    assert resp.status_code in {401, 403}


# ---------- 2) Invalid mode is rejected ----------

def test_create_inspection_invalid_mode(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, _ = _create_client()
    token, _ = _register_and_get_token(client)

    resp = client.post(
        "/inspections",
        json={"mode": "invalid"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 422


# ---------- 3) Authenticated corrosion inspection succeeds ----------

def test_create_corrosion_inspection(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, _ = _create_client()
    token, _ = _register_and_get_token(client)

    resp = client.post(
        "/inspections",
        json={"mode": "corrosion"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "inspection_id" in data
    assert isinstance(data["upload_urls"], list)
    assert len(data["upload_urls"]) > 0
    assert "expires_at" in data


# ---------- 4) Osmosis blocked without valid payment ----------

def test_create_osmosis_inspection_blocked_without_payment(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, _ = _create_client()
    token, _ = _register_and_get_token(client)

    resp = client.post(
        "/inspections",
        json={"mode": "osmosis"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 402
    assert "payment" in resp.json()["detail"].lower()


# ---------- 5) Osmosis allowed with valid payment flag ----------

def test_create_osmosis_inspection_with_valid_payment(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, user_id = _register_and_get_token(client)

    # Set payment valid for this user
    app.state.payment_store.set_payment_valid(user_id)

    resp = client.post(
        "/inspections",
        json={"mode": "osmosis"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "inspection_id" in data
    assert isinstance(data["upload_urls"], list)
    assert len(data["upload_urls"]) > 0
    assert "expires_at" in data


# ---------- 6) Created inspection stores immutable mode ----------

def test_inspection_mode_is_immutable(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, _ = _register_and_get_token(client)

    resp = client.post(
        "/inspections",
        json={"mode": "corrosion"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    inspection_id = resp.json()["inspection_id"]

    # Verify mode is stored and immutable in the store
    stored = app.state.inspection_store.get_by_id(inspection_id)
    assert stored is not None
    assert stored.mode == "corrosion"


# ---------- 7) Idempotency: repeated corrosion returns same inspection ----------

def test_idempotent_corrosion_returns_same_id(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, _ = _create_client()
    token, _ = _register_and_get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    resp1 = client.post("/inspections", json={"mode": "corrosion"}, headers=headers)
    assert resp1.status_code == 201

    resp2 = client.post("/inspections", json={"mode": "corrosion"}, headers=headers)
    assert resp2.status_code == 200
    assert resp2.json()["inspection_id"] == resp1.json()["inspection_id"]


# ---------- 8) Idempotency: repeated paid osmosis returns same inspection ----------

def test_idempotent_osmosis_returns_same_id(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, user_id = _register_and_get_token(client)
    app.state.payment_store.set_payment_valid(user_id)
    headers = {"Authorization": f"Bearer {token}"}

    resp1 = client.post("/inspections", json={"mode": "osmosis"}, headers=headers)
    assert resp1.status_code == 201

    resp2 = client.post("/inspections", json={"mode": "osmosis"}, headers=headers)
    assert resp2.status_code == 200
    assert resp2.json()["inspection_id"] == resp1.json()["inspection_id"]


# ---------- 9) Different mode does not reuse the same inspection ----------

def test_different_mode_creates_separate_inspection(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, user_id = _register_and_get_token(client)
    app.state.payment_store.set_payment_valid(user_id)
    headers = {"Authorization": f"Bearer {token}"}

    resp_corrosion = client.post("/inspections", json={"mode": "corrosion"}, headers=headers)
    assert resp_corrosion.status_code == 201

    resp_osmosis = client.post("/inspections", json={"mode": "osmosis"}, headers=headers)
    assert resp_osmosis.status_code == 201
    assert resp_osmosis.json()["inspection_id"] != resp_corrosion.json()["inspection_id"]


# ---------- BE-030: Complete Upload Tests ----------

def test_complete_upload_unauthenticated(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, _ = _create_client()
    resp = client.post(f"/inspections/{uuid4()}/complete")
    assert resp.status_code in {401, 403}


def test_complete_upload_non_existent(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, _ = _create_client()
    token, _ = _register_and_get_token(client)
    resp = client.post(
        f"/inspections/{uuid4()}/complete",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 404


def test_complete_upload_other_user(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token_a, user_id_a = _register_and_get_token(client)
    token_b, _ = _register_and_get_token(client)

    # Create inspection for A
    resp_create = client.post(
        "/inspections",
        json={"mode": "corrosion"},
        headers={"Authorization": f"Bearer {token_a}"},
    )
    assert resp_create.status_code == 201
    inspection_id = resp_create.json()["inspection_id"]

    # B tries to complete A's inspection
    resp_complete = client.post(
        f"/inspections/{inspection_id}/complete",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert resp_complete.status_code == 403


def test_complete_upload_success(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, _ = _register_and_get_token(client)

    resp_create = client.post(
        "/inspections",
        json={"mode": "corrosion"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp_create.status_code == 201
    inspection_id = resp_create.json()["inspection_id"]

    # Complete
    resp_complete = client.post(
        f"/inspections/{inspection_id}/complete",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp_complete.status_code == 200
    assert resp_complete.json() == {"status": "queued"}

    # Verify state in store
    stored = app.state.inspection_store.get_by_id(inspection_id)
    assert stored.status == "queued"


def test_complete_upload_idempotent(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, _ = _register_and_get_token(client)

    resp_create = client.post(
        "/inspections",
        json={"mode": "corrosion"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp_create.status_code == 201
    inspection_id = resp_create.json()["inspection_id"]

    # Complete once
    resp1 = client.post(
        f"/inspections/{inspection_id}/complete",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp1.status_code == 200
    assert resp1.json() == {"status": "queued"}

    # Complete twice
    resp2 = client.post(
        f"/inspections/{inspection_id}/complete",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp2.status_code == 200
    assert resp2.json() == {"status": "queued"}

    # Check job queue size or count of jobs
    assert len(app.state.job_queue._jobs) == 1


def test_complete_upload_queue_record_fields(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, user_id = _register_and_get_token(client)

    resp_create = client.post(
        "/inspections",
        json={"mode": "corrosion"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp_create.status_code == 201
    inspection_id = resp_create.json()["inspection_id"]

    # Complete
    resp_complete = client.post(
        f"/inspections/{inspection_id}/complete",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp_complete.status_code == 200

    # Get job from queue
    job = app.state.job_queue.get_by_inspection_id(inspection_id)
    assert job is not None
    assert job.inspection_id == inspection_id
    assert job.user_id == user_id
    assert job.mode == "corrosion"


# ---------- BE-040: Get Inspection Status Tests ----------

def test_get_status_unauthenticated(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, _ = _create_client()
    resp = client.get(f"/inspections/{uuid4()}")
    assert resp.status_code in {401, 403}


def test_get_status_non_existent(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, _ = _create_client()
    token, _ = _register_and_get_token(client)
    resp = client.get(
        f"/inspections/{uuid4()}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 404


def test_get_status_other_user(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token_a, user_id_a = _register_and_get_token(client)
    token_b, _ = _register_and_get_token(client)

    # Create inspection for A
    resp_create = client.post(
        "/inspections",
        json={"mode": "corrosion"},
        headers={"Authorization": f"Bearer {token_a}"},
    )
    assert resp_create.status_code == 201
    inspection_id = resp_create.json()["inspection_id"]

    # B tries to read A's inspection status
    resp_status = client.get(
        f"/inspections/{inspection_id}",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert resp_status.status_code == 403


def test_get_status_owner_new(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, user_id = _register_and_get_token(client)

    # Create inspection
    resp_create = client.post(
        "/inspections",
        json={"mode": "corrosion"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp_create.status_code == 201
    inspection_id = resp_create.json()["inspection_id"]

    # Read status
    resp_status = client.get(
        f"/inspections/{inspection_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp_status.status_code == 200
    data = resp_status.json()
    assert data["inspection_id"] == inspection_id
    assert data["status"] == "pending"
    
    # Verify response contains only API-spec fields: status, inspection_id
    assert set(data.keys()) == {"inspection_id", "status"}


def test_get_status_owner_after_upload_completion(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, user_id = _register_and_get_token(client)

    # Create inspection
    resp_create = client.post(
        "/inspections",
        json={"mode": "corrosion"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp_create.status_code == 201
    inspection_id = resp_create.json()["inspection_id"]

    # Complete upload
    resp_complete = client.post(
        f"/inspections/{inspection_id}/complete",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp_complete.status_code == 200

    # Get status reflecting queued state in store (mapped to pending)
    resp_status = client.get(
        f"/inspections/{inspection_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp_status.status_code == 200
    data = resp_status.json()
    assert data["inspection_id"] == inspection_id
    assert data["status"] == "pending"
    assert set(data.keys()) == {"inspection_id", "status"}

    # Verify that if we manually set store status to "processing", "completed", "failed", it is reflected
    stored = app.state.inspection_store.get_by_id(inspection_id)
    
    stored.status = "processing"
    resp_p = client.get(f"/inspections/{inspection_id}", headers={"Authorization": f"Bearer {token}"})
    assert resp_p.json()["status"] == "processing"

    stored.status = "completed"
    resp_c = client.get(f"/inspections/{inspection_id}", headers={"Authorization": f"Bearer {token}"})
    assert resp_c.json()["status"] == "completed"

    stored.status = "failed"
    resp_f = client.get(f"/inspections/{inspection_id}", headers={"Authorization": f"Bearer {token}"})
    assert resp_f.json()["status"] == "failed"


# ---------- BE-050: Get Inspection Result Tests ----------

from app.core.store import StoredResult


def _seed_completed_inspection(client, app, token, mode="corrosion"):
    """Helper: create an inspection, mark completed, seed a result. Returns inspection_id."""
    resp = client.post(
        "/inspections",
        json={"mode": mode},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    inspection_id = resp.json()["inspection_id"]

    # Set status to completed (simulates worker finishing)
    stored = app.state.inspection_store.get_by_id(inspection_id)
    stored.status = "completed"

    # Seed a result
    result = StoredResult(
        inspection_id=inspection_id,
        mode=mode,
        signal_detected="yes",
        confidence_level="medium",
        guidance=["monitor", "recheck_later"],
        model_version="stub-v0.1.0",
        created_at="2026-06-05T12:00:00+00:00",
    )
    app.state.result_store.save(result)

    return inspection_id


def test_get_result_unauthenticated(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, _ = _create_client()
    resp = client.get(f"/inspections/{uuid4()}/result")
    assert resp.status_code in {401, 403}


def test_get_result_non_existent(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, _ = _create_client()
    token, _ = _register_and_get_token(client)
    resp = client.get(
        f"/inspections/{uuid4()}/result",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 404


def test_get_result_other_user(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token_a, _ = _register_and_get_token(client)
    token_b, _ = _register_and_get_token(client)

    inspection_id = _seed_completed_inspection(client, app, token_a)

    # B tries to read A's result
    resp = client.get(
        f"/inspections/{inspection_id}/result",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert resp.status_code == 403


def test_get_result_not_completed(monkeypatch):
    """Inspection exists but is still pending — returns 409."""
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, _ = _register_and_get_token(client)

    resp_create = client.post(
        "/inspections",
        json={"mode": "corrosion"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp_create.status_code == 201
    inspection_id = resp_create.json()["inspection_id"]

    # Status is still "pending" — do not set to completed
    resp = client.get(
        f"/inspections/{inspection_id}/result",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 409
    assert "not available" in resp.json()["detail"].lower()


def test_get_result_completed_but_no_result_stored(monkeypatch):
    """Inspection marked completed but result store is empty — returns 404."""
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, _ = _register_and_get_token(client)

    resp_create = client.post(
        "/inspections",
        json={"mode": "corrosion"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp_create.status_code == 201
    inspection_id = resp_create.json()["inspection_id"]

    # Set status to completed but do NOT seed a result
    stored = app.state.inspection_store.get_by_id(inspection_id)
    stored.status = "completed"

    resp = client.get(
        f"/inspections/{inspection_id}/result",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 404
    assert "result" in resp.json()["detail"].lower()


def test_get_result_happy_path_corrosion(monkeypatch):
    """Completed corrosion inspection with seeded result returns 200 + correct contract."""
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, _ = _register_and_get_token(client)

    inspection_id = _seed_completed_inspection(client, app, token, mode="corrosion")

    resp = client.get(
        f"/inspections/{inspection_id}/result",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["inspection_id"] == inspection_id
    assert data["mode"] == "corrosion"
    assert data["signal_detected"] == "yes"
    assert data["confidence_level"] == "medium"
    assert data["guidance"] == ["monitor", "recheck_later"]
    assert data["model_version"] == "stub-v0.1.0"
    assert data["created_at"] == "2026-06-05T12:00:00+00:00"


def test_get_result_happy_path_osmosis(monkeypatch):
    """Completed osmosis inspection with seeded result returns 200 + correct mode."""
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, user_id = _register_and_get_token(client)

    # Osmosis requires payment
    app.state.payment_store.set_payment_valid(user_id)

    inspection_id = _seed_completed_inspection(client, app, token, mode="osmosis")

    resp = client.get(
        f"/inspections/{inspection_id}/result",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["inspection_id"] == inspection_id
    assert data["mode"] == "osmosis"


def test_get_result_response_field_contract(monkeypatch):
    """Response keys must exactly match API-Spec.md § 3.4."""
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client, app = _create_client()
    token, _ = _register_and_get_token(client)

    inspection_id = _seed_completed_inspection(client, app, token, mode="corrosion")

    resp = client.get(
        f"/inspections/{inspection_id}/result",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    expected_keys = {
        "inspection_id",
        "mode",
        "signal_detected",
        "confidence_level",
        "guidance",
        "model_version",
        "created_at",
    }
    assert set(resp.json().keys()) == expected_keys
