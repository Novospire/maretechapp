from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import create_app


def _create_client():
    app = create_app()
    return TestClient(app)


def _register_and_get_token(client: TestClient) -> str:
    register_payload = {"email": "policy@example.com", "password": "password123"}
    register_response = client.post("/auth/register", json=register_payload)
    assert register_response.status_code == 201
    return register_response.json()["token"]["access_token"]


def test_capture_policy_unauthenticated():
    client = _create_client()
    response = client.get("/capture-policy/corrosion")
    assert response.status_code in {401, 403}


def test_capture_policy_corrosion_authenticated(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client = _create_client()
    token = _register_and_get_token(client)

    response = client.get("/capture-policy/corrosion", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {
        "mode": "corrosion",
        "free_points": 5,
        "max_points": 10,
        "angles_per_point": 3,
    }


def test_capture_policy_osmosis_authenticated(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client = _create_client()
    token = _register_and_get_token(client)

    response = client.get("/capture-policy/osmosis", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    payload = response.json()
    assert payload["error_code"] == "POLICY_NOT_DEFINED"


def test_capture_policy_invalid_mode(monkeypatch):
    monkeypatch.setenv("MARETECH_JWT_SECRET", "test-secret")
    client = _create_client()
    token = _register_and_get_token(client)

    response = client.get("/capture-policy/invalid", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422
