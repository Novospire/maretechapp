from __future__ import annotations

from fastapi import FastAPI

from app.api import auth, capture_policy
from app.core.store import InMemoryUserStore


user_store = InMemoryUserStore()


def create_app() -> FastAPI:
    app = FastAPI(title="Maretech API", version="0.1.0")
    app.include_router(auth.router)
    app.include_router(capture_policy.router)
    return app


app = create_app()
