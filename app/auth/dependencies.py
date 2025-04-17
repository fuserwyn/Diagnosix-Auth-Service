from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth import AuthService
from app.models.user import User
from app.db import async_session_maker
from app.constants.roles import UserRole
from typing import Union

bearer_scheme = HTTPBearer(auto_error=False)


async def get_db():
    async with async_session_maker() as session:
        yield session


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    if credentials is None or not credentials.scheme.lower() == "bearer":
        raise HTTPException(status_code=403, detail="Authorization required")
    return await AuthService(db).get_current_user(credentials.credentials)


def role_required(required_roles: list[Union[str, UserRole]]):
    def checker(user: User = Depends(get_current_user)):
        if user.role not in required_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")
        return user
    return checker