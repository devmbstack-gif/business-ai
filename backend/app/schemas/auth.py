from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    full_name: Optional[str] = Field(default=None, max_length=255)


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class GuestSessionRequest(BaseModel):
    guest_session_id: Optional[str] = Field(default=None, max_length=100)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    is_guest: bool = False
    is_admin: bool = False


class UserResponse(BaseModel):
    id: int
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: str
    plan: str
    is_guest: bool
    is_admin: bool
    created_at: datetime

    model_config = {"from_attributes": True}
