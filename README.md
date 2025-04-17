# Diagnosix Auth-Service 🩺

Микросервис аутентификации для Diagnosix MVP.

Позволяет:
- ✅ Регистрировать пользователей (`/register`)
- 🔐 Выполнять вход с генерацией JWT токенов (`/login`)
- 👤 Получать информацию о текущем пользователе (`/me`)
- 🛡 Контролировать доступ по ролям (`/dashboard`, только для `admin`)

---

## 📦 Стек технологий

- **FastAPI** — веб-фреймворк
- **PostgreSQL** — СУБД (через `asyncpg`)
- **SQLAlchemy 2.0** + Alembic — ORM и миграции
- **Pydantic v2** — схемы и валидация
- **JWT** (`python-jose`) — для токенов
- **Docker + Docker Compose**
- **Pytest** — тестирование
- **Pre-commit hooks** — качество кода

---

## 🧪 Возможности API

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| `POST` | `/register` | Регистрация нового пользователя |
| `POST` | `/login` | Аутентификация, получение токенов |
| `GET` | `/me` | Информация о текущем пользователе |
| `GET` | `/dashboard` | Только для админов (по JWT-ролям) |

---

## 🚀 Запуск через Docker

```bash
git clone git@github.com:fuserwyn/Diagnosix-Auth-Service.git
cd Diagnosix-Auth-Service
cp .env.example .env
make up
```

После запуска сервис доступен по адресу: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📂 Пример `.env`

```env
DB_HOST=db
DB_PORT=5432
DB_NAME=auth_db
DB_USER=postgres
DB_PASSWORD=postgres
SECRET_KEY=supersecret
```

---

## 🧪 Тестирование

### Локально:
```bash
make test
```

### В Docker:
```bash
docker-compose exec web bash
pytest -s
```

---

## 📬 Примеры curl-запросов

### 🔐 Регистрация

```bash
curl -X POST http://localhost:8000/register \
 -H "Content-Type: application/json" \
 -d '{"email": "test@example.com", "password": "qwerty123", "role": "doctor"}'
```

### 🔑 Вход

```bash
curl -X POST http://localhost:8000/login \
 -H "Content-Type: application/json" \
 -d '{"email": "test@example.com", "password": "qwerty123"}'
```

### 👤 Получить текущего пользователя

```bash
curl -X GET http://localhost:8000/me \
 -H "Authorization: Bearer <ваш_токен>"
```

---

## 🧭 Структура проекта

```
auth_service/
├── app/
│   ├── main.py               # Инициализация FastAPI
│   ├── auth/                 # JWT и зависимости
│   ├── routes/               # Эндпоинты
│   ├── schemas/              # Pydantic-схемы
│   ├── services/             # Логика авторизации
│   ├── models/               # SQLAlchemy-модели
│   ├── core/config.py        # Конфигурация (pydantic-settings)
│   ├── repositories/         # Слой доступа к данным (UserRepo и базовый репозиторий)
│   ├── database/db.py        # Асинхронное подключение к БД
│   └── tests/                # Тесты внутри app/
├── migrations/               # Миграции
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🛡 Безопасность

- Валидация паролей и ролей через Pydantic
- Хеширование паролей (`passlib`)
- JWT с поддержкой ролей (`admin`, `doctor`, `patient`)
- Ограничения доступа через декораторы (`Depends(role_required(...))`)

---

## 🧪 Покрытие тестами

- `register`, `login`, `me`, `dashboard` протестированы
- Используется `pytest`, `pytest-asyncio`, `httpx`

---

## 🧠 Особенности реализации

- Используется UUID в качестве `id`
- Асинхронный стек (FastAPI + asyncpg + SQLAlchemy 2.0)
- JWT access/refresh токены
- Полностью разделённые слои: `routes → services → repo`

---
## 📜 Миграции Alembic

Миграции хранятся в директории `migrations/`. Для их запуска:

### 🔼 Создание новой миграции

В Docker-контейнере:
```bash
alembic revision --autogenerate -m "your message"
```

### ⬆️ Применение миграций

```bash
alembic upgrade head
```

---

## 🛠 Makefile (опционально)

Для удобства можно использовать `Makefile`:

```makefile
migrations:
	alembic revision --autogenerate

migrate:
	alembic upgrade head
```

### Примеры использования:

```bash
make run
make migrate
make test
```
Enjoy 👨‍⚕️✨