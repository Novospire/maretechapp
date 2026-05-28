from __future__ import annotations

import logging

from fastapi import FastAPI

from app.api import auth, capture_policy, health, inspections
from app.core.store import InMemoryInspectionStore, InMemoryJobQueue, InMemoryPaymentStore, InMemoryUserStore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("maretech")

def create_app(user_store: InMemoryUserStore | None = None) -> FastAPI:
    app = FastAPI(title="Maretech API", version="0.1.0")
    app.state.user_store = user_store or InMemoryUserStore()
    app.state.inspection_store = InMemoryInspectionStore()
    app.state.payment_store = InMemoryPaymentStore()
    app.state.job_queue = InMemoryJobQueue()
    app.state.token_revocation_list = set()
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(capture_policy.router)
    app.include_router(inspections.router)
    logger.info("Maretech API application created")
    return app


app = create_app()
