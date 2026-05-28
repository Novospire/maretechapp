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

