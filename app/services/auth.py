from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt import decode_token
from app.models.user import User
from app.repositories.user_repo import user_repo


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_current_user(self, token: str) -> User:
        payload = decode_token(token)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user = await user_repo.get_user_by_email(self.db, payload["sub"])
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user
