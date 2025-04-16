# Diagnosix Auth-Service

Auth microservice for Diagnosix MVP. Provides:

- ✅ User registration `/register`
- 🔐 Login and JWT authentication `/login`
- 👤 Get current user `/me`

---

## 🚀 Tech Stack

- **FastAPI**
- **PostgreSQL** (async via `asyncpg`)
- **SQLAlchemy 2.0** + Alembic
- **Pydantic v2**
- **Docker / Docker Compose**
- **Pytest** + `httpx` for async API tests

---

## 🐳 Docker Quickstart

```bash
git clone <this-repo>
cd auth-service
cp .env.example .env

# Build and run
docker-compose up --build
```

Then open: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📄 .env Example

```env
DB_HOST=db
DB_PORT=5432
DB_NAME=auth_db
DB_USER=postgres
DB_PASSWORD=postgres
SECRET_KEY=supersecret
```

---

## 🧪 Running Tests

### ▶️ Locally
```bash
PYTHONPATH=. pytest -v
```

### 🐳 Inside Docker
```bash
docker-compose exec web bash
PYTHONPATH=/code pytest -v
```

---

## 📬 API Examples (curl)

### 🔐 Register
```bash
curl -X POST http://localhost:8000/register \
 -H "Content-Type: application/json" \
 -d '{"email": "test@example.com", "password": "testpass", "role": "doctor"}'
```

### 🔑 Login
```bash
curl -X POST http://localhost:8000/login \
 -H "Content-Type: application/json" \
 -d '{"email": "test@example.com", "password": "testpass"}'
```

### 👤 Get current user
```bash
curl -X GET http://localhost:8000/me \
 -H "Authorization: Bearer <your_token_here>"
```

---

## 🧭 Project Structure

```bash
auth_service/
├── app/
│   ├── main.py             # FastAPI app init
│   ├── db.py               # async SQLAlchemy setup
│   ├── models/             # SQLAlchemy models (User)
│   ├── schemas/            # Pydantic schemas
│   ├── routes/             # API endpoints
│   ├── services/           # Business logic
│   ├── auth/               # JWT logic & dependencies
│   └── core/config.py      # Settings (via pydantic-settings)
│
├── tests/
│   ├── conftest.py         # Fixtures (client, cleanup)
│   ├── test_auth.py        # /register and /login
│   └── test_api.py        # /me
│
├── alembic/                # DB migrations
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🧠 Author Notes

- Uses UUID as primary key
- Fully async
- Covers main flows with tests
- Split architecture: routers → services → repos

Enjoy hacking 👨‍⚕️✨
