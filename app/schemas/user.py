from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "patient"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    role: str

    class Config:
        from_attributes = True