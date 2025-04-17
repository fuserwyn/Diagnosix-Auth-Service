from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from app.schemas.user import UserCreate, UserLogin
from app.schemas.token import Token
from app.repositories.user_repo import user_repo
from app.auth.jwt import create_access_token, create_refresh_token
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    @staticmethod
    async def register_user(user: UserCreate, db: AsyncSession):
        db_user = await user_repo.get_user_by_email(db, user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_pw = pwd_context.hash(user.password)
        new_user = User(email=user.email, hashed_password=hashed_pw, role=user.role)
        return await user_repo.create(db, new_user)

    @staticmethod
    async def authenticate_user(user: UserLogin, db: AsyncSession):
        db_user = await user_repo.get_user_by_email(db, user.email)
        if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token({"sub": db_user.email, "role": db_user.role})
        return {"access_token": token, "token_type": "bearer"}

    @staticmethod
    async def authenticate_user(user: UserLogin, db: AsyncSession) -> Token:
        db_user = await user_repo.get_user_by_email(db, user.email)
        if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token: str = create_access_token({"sub": db_user.email, "role": db_user.role})
        refresh_token: str = create_refresh_token({"sub": db_user.email})

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, update_data: dict):
        user = await user_repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return await user_repo.update(db, user, update_data)