from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.jwt import decode_token
from app.repositories.user_repo import user_repo


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_current_user(self, token: str):
        payload = decode_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = await user_repo.get_user_by_email(self.db, payload["sub"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
