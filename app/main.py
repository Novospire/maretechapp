from __future__ import annotations

from fastapi import FastAPI

from app.api import auth, capture_policy
from app.core.store import InMemoryUserStore

def create_app(user_store: InMemoryUserStore | None = None) -> FastAPI:
    app = FastAPI(title="Maretech API", version="0.1.0")
    app.state.user_store = user_store or InMemoryUserStore()
    app.state.token_revocation_list = set()
    app.include_router(auth.router)
    app.include_router(capture_policy.router)
    return app


app = create_app()
