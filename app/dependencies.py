from __future__ import annotations

from typing import Set

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError

from app.core.security import decode_access_token
from app.core.store import InMemoryUserStore


bearer_scheme = HTTPBearer()

def get_user_store(request: Request) -> InMemoryUserStore:
    return request.app.state.user_store


def get_token_revocation_list(request: Request) -> Set[str]:
    return request.app.state.token_revocation_list


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    store: InMemoryUserStore = Depends(get_user_store),
    token_revocation_list: Set[str] = Depends(get_token_revocation_list),
):
    token = credentials.credentials
    if token in token_revocation_list:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked")
    try:
        payload = decode_access_token(token)
    except InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = store.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
