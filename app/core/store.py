from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional
from uuid import uuid4


@dataclass
class StoredUser:
    id: str
    email: str
    password_hash: str


class InMemoryUserStore:
    def __init__(self) -> None:
        self._users_by_email: Dict[str, StoredUser] = {}
        self._users_by_id: Dict[str, StoredUser] = {}

    def get_by_email(self, email: str) -> Optional[StoredUser]:
        return self._users_by_email.get(email.lower())

    def get_by_id(self, user_id: str) -> Optional[StoredUser]:
        return self._users_by_id.get(user_id)

    def create_user(self, email: str, password_hash: str) -> StoredUser:
        user = StoredUser(id=str(uuid4()), email=email.lower(), password_hash=password_hash)
        self._users_by_email[user.email] = user
        self._users_by_id[user.id] = user
        return user
