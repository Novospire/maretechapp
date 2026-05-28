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
