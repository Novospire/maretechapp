from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import create_app


def test_auth_smoke_flow(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    app = create_app()
    client = TestClient(app)

    register_payload = {"email": "user@example.com", "password": "password123"}
    register_response = client.post("/auth/register", json=register_payload)
    assert register_response.status_code == 201
    register_token = register_response.json()["token"]["access_token"]

    login_response = client.post("/auth/login", json=register_payload)
    assert login_response.status_code == 200
    token = login_response.json()["token"]["access_token"]
    assert register_token != token

    me_response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_response.status_code == 200

    logout_response = client.post("/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert logout_response.status_code == 204

    revoked_response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert revoked_response.status_code == 401

    me_response_second_token = client.get(
        "/auth/me", headers={"Authorization": f"Bearer {register_token}"}
    )
    assert me_response_second_token.status_code == 200


def test_no_global_user_store_leakage(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    first_client = TestClient(create_app())
    second_client = TestClient(create_app())

    register_payload = {"email": "leak-test@example.com", "password": "password123"}
    register_response = first_client.post("/auth/register", json=register_payload)
    assert register_response.status_code == 201

    login_response = second_client.post("/auth/login", json=register_payload)
    assert login_response.status_code == 401
