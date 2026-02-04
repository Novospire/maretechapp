from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.core.store import InMemoryUserStore
from app.dependencies import (
    bearer_scheme,
    get_current_user,
    get_token_revocation_list,
    get_user_store,
)
from app.schemas import AuthResponse, Token, UserCreate, UserLogin, UserOut


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, store: InMemoryUserStore = Depends(get_user_store)):
    existing = store.get_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user = store.create_user(payload.email, hash_password(payload.password))
    token = create_access_token(user.id)
    return AuthResponse(user=UserOut(id=user.id, email=user.email), token=Token(access_token=token))


@router.post("/login", response_model=AuthResponse)
async def login(payload: UserLogin, store: InMemoryUserStore = Depends(get_user_store)):
    user = store.get_by_email(payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(user.id)
    return AuthResponse(user=UserOut(id=user.id, email=user.email), token=Token(access_token=token))


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    credentials=Depends(bearer_scheme),
    current_user=Depends(get_current_user),
    token_revocation_list=Depends(get_token_revocation_list),
):
    token_revocation_list.add(credentials.credentials)
    return None


@router.get("/me", response_model=UserOut)
async def me(current_user=Depends(get_current_user)):
    return UserOut(id=current_user.id, email=current_user.email)
