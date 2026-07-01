from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional, Literal


ROLES = Literal["viewer", "analyst", "admin"]


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: ROLES = "analyst"


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True


class UserWithScopes(UserResponse):
    scopes: list[str] = []


# Pydantic v2 field_validator support: keep username/email normalization in routers/services.
