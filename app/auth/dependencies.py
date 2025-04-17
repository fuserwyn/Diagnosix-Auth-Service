from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth import AuthService
from app.models.user import User
from app.db import async_session_maker

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