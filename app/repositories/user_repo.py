from typing import Optional

from passlib.hash import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import User
from app.repositories.base import BaseRepo
from app.schemas.user import UserCreate


class UserRepo(BaseRepo[User]):
    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create_user(self, db: AsyncSession, user: UserCreate) -> User:
        hashed_pw = bcrypt.hash(user.password)
        db_user = User(email=user.email, hashed_password=hashed_pw, role=user.role)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user


user_repo = UserRepo(User)
