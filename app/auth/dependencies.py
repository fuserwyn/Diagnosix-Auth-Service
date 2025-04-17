from typing import AsyncGenerator, Callable, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import async_session_maker
from app.models.user import User
from app.services.auth import AuthService
from app.utils.constants.roles import UserRole

bearer_scheme = HTTPBearer(auto_error=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: AsyncSession = Depends(get_db)  # noqa: B008
) -> User:
    if credentials is None or not credentials.scheme.lower() == "bearer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Authorization required")
    return await AuthService(db).get_current_user(credentials.credentials)


def role_required(required_roles: list[Union[str, UserRole]]) -> Callable[..., User]:
    def checker(user: User = Depends(get_current_user)) -> User:  # noqa: B008
        if user.role not in required_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")
        return user

    return checker
