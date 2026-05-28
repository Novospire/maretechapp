from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import create_app


def test_health_returns_ok():
    """BE-000 acceptance: /health returns {"status": "ok"}."""
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_no_auth_required():
    """Health endpoint must be reachable without a bearer token."""
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
