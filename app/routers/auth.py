from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, get_db, role_required
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.services.user import UserService
from app.utils.constants.roles import UserRole

router = APIRouter()


@router.post(
    "/register",
    response_model=UserOut,
    summary="Регистрация нового пользователя",
    description="""
Создаёт нового пользователя в системе.

- Требуется email, пароль и роль (`patient`, `doctor`, `admin`)
- Пароль должен содержать хотя бы одну букву и цифру, от 6 до 32 символов
""",
    tags=["Аутентификация"],
)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserOut:  # noqa: B008
    return await UserService.register_user(user, db)


@router.post(
    "/login",
    response_model=Token,
    summary="Аутентификация пользователя",
    description="""
Проверяет email и пароль, и возвращает JWT access/refresh токены.

- Используется bcrypt для хеширования пароля
- Access-токен имеет ограниченное время жизни
""",
    tags=["Аутентификация"],
)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)) -> Token:  # noqa: B008
    return await UserService.authenticate_user(user, db)


@router.get(
    "/me",
    response_model=UserOut,
    summary="Получить текущего пользователя",
    description="Возвращает информацию о пользователе, извлечённом из JWT access токена.",
    tags=["Пользователь"],
)
async def me(current_user: UserOut = Depends(get_current_user)) -> UserOut:  # noqa: B008
    return current_user


@router.get(
    "/dashboard",
    summary="Панель администратора",
    description="Доступ разрешён только пользователям с ролью `admin`.",
    tags=["Админ"],
    dependencies=[Depends(role_required([UserRole.ADMIN.value]))],
)
async def dashboard() -> dict[str, str]:
    return {"message": "Welcome, admin"}
