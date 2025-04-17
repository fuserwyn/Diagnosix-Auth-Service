from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.routers import auth
from app.utils.exceptions import validation_exception_handler

app = FastAPI(
    title="Diagnosix Auth Service",
    description="""
📋 **Diagnosix Auth Service**

Микросервис для аутентификации пользователей в системе Diagnosix.

### Возможности:

- ✅ Регистрация пользователей (`/register`)
- 🔐 Аутентификация и JWT (`/login`)
- 👤 Получение информации о текущем пользователе (`/me`)
- 🛡 Доступ по ролям (`/dashboard`)

> Все ответы и запросы оформлены в виде Pydantic-схем.
""",
    version="1.0.0",
    contact={"name": "Diagnosix Dev Team"},
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(auth.router)
