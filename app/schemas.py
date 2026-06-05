from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AuthResponse(BaseModel):
    user: UserOut
    token: Token


class InspectionCreate(BaseModel):
    mode: str = Field(..., pattern=r"^(osmosis|corrosion)$")


class InspectionCreated(BaseModel):
    inspection_id: str
    upload_urls: list[str]
    expires_at: str


class CompleteResponse(BaseModel):
    status: str


class InspectionStatusResponse(BaseModel):
    inspection_id: str
    status: str


class InspectionResultResponse(BaseModel):
    inspection_id: str
    mode: str
    signal_detected: str
    confidence_level: str
    guidance: list[str]
    model_version: str
    created_at: str

