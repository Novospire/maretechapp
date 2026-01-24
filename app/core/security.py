from __future__ import annotations

import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from uuid import uuid4

import jwt


def _get_secret() -> str:
    secret = os.getenv("MARETECH_JWT_SECRET")
    if not secret:
        raise RuntimeError("MARETECH_JWT_SECRET is required for JWT operations")
    return secret


def hash_password(password: str) -> str:
    salt = os.getenv("MARETECH_PASSWORD_SALT", "dev-salt")
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000)
    return digest.hex()


def verify_password(password: str, password_hash: str) -> bool:
    computed = hash_password(password)
    return hmac.compare_digest(computed, password_hash)


def create_access_token(subject: str, expires_in_minutes: int = 60) -> str:
    now = datetime.now(timezone.utc)
    payload: Dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expires_in_minutes)).timestamp()),
        "jti": uuid4().hex,
    }
    return jwt.encode(payload, _get_secret(), algorithm="HS256")


def decode_access_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, _get_secret(), algorithms=["HS256"])
