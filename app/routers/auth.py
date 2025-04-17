from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.schemas.token import Token
from app.auth.dependencies import get_db, get_current_user, role_required
from app.services.user import UserService
from app.constants.roles import UserRole

router = APIRouter()


@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserOut:
    return await UserService.register_user(user, db)


@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)) -> Token:
    return await UserService.authenticate_user(user, db)


@router.get("/me", response_model=UserOut)
async def me(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    return current_user


@router.get("/dashboard", dependencies=[Depends(role_required([UserRole.ADMIN.value]))])
async def dashboard() -> dict[str, str]:
    return {"message": "Welcome, admin"}