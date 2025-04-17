from fastapi import APIRouter, Depends, status
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
    description="""Создаёт нового пользователя в системе.

- Требуется email, пароль и роль (patient, doctor, admin)
- Возвращает зарегистрированного пользователя
""",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Email уже зарегистрирован"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации (например, плохой пароль или неизвестная роль)"
        },
    },
    tags=["Аутентификация"],
)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserOut:  # noqa  B008
    return await UserService.register_user(user, db)


@router.post(
    "/login",
    response_model=Token,
    summary="Аутентификация пользователя",
    description="""Проверяет email и пароль, возвращает JWT токены (access и refresh).

- Использует bcrypt для проверки пароля
- Если данные неверны — возвращает 401
""",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Неверные учётные данные"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Ошибка валидации"},
    },
    tags=["Аутентификация"],
)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)) -> Token:  # noqa  B008
    return await UserService.authenticate_user(user, db)


@router.get(
    "/me",
    response_model=UserOut,
    summary="Текущий пользователь",
    description="Возвращает информацию о текущем пользователе по JWT токену.",
    responses={
        status.HTTP_403_FORBIDDEN: {"description": "Отсутствует или недействительный токен"},
    },
    tags=["Пользователь"],
)
async def me(current_user: UserOut = Depends(get_current_user)) -> UserOut:  # noqa  B008
    return current_user


@router.get(
    "/dashboard",
    summary="Панель администратора",
    description="Только для пользователей с ролью 'admin'.",
    responses={
        status.HTTP_403_FORBIDDEN: {"description": "Доступ запрещён: роль недостаточна"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Отсутствует авторизация"},
    },
    tags=["Админ"],
    dependencies=[Depends(role_required([UserRole.ADMIN.value]))],
)
async def dashboard() -> dict[str, str]:
    return {"message": "Welcome, admin"}
