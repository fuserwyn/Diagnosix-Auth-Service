import re
from typing import Any
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator

from app.utils.constants.roles import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.PATIENT

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        if len(v) > 32:
            raise ValueError("Password must not exceed 32 characters")
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Password must include at least one letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must include at least one digit")
        return v

    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, value: Any) -> UserRole:
        try:
            return UserRole(value)
        except ValueError:
            allowed = [role.value for role in UserRole]
            raise ValueError(f"Invalid role: '{value}'. Must be one of: {allowed}")


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True
