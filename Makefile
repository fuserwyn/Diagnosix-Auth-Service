ENV_FILE ?= .env

up:
	ENV_FILE=$(ENV_FILE) docker-compose up -d --build

down:
	docker-compose down

run:
	ENV_FILE=$(ENV_FILE) docker-compose up -d --build
	docker-compose exec web bash

rebuild:
	docker-compose down --volumes --remove-orphans
	ENV_FILE=$(ENV_FILE) docker-compose up -d --build

migrations:
	alembic revision --autogenerate

migrate:
	alembic upgrade head

test:
	@echo "📦 Preparing test database..."
	@DB_NAME=$$(grep TEST_DB_NAME .env | cut -d '=' -f2); \
	DB_USER=$$(grep TEST_DB_USER .env | cut -d '=' -f2); \
	env $$(grep ^TEST_ .env | sed 's/^TEST_//') docker-compose exec db psql -U $$DB_USER -tc "SELECT 1 FROM pg_database WHERE datname='$$DB_NAME'" | grep -q 1 || \
	env $$(grep ^TEST_ .env | sed 's/^TEST_//') docker-compose exec db psql -U $$DB_USER -c "CREATE DATABASE $$DB_NAME;"; \
	echo "⚙️ Resetting schema..."; \
	env $$(grep ^TEST_ .env | sed 's/^TEST_//') docker-compose exec db psql -U $$DB_USER -d $$DB_NAME -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL PRIVILEGES ON SCHEMA public TO $$DB_USER;"

	@echo "🚀 Running tests..."
	env $$(grep ^TEST_ .env | sed 's/^TEST_//') docker-compose exec web pytest -s -v

	@echo "🧹 Dropping test database..."
	@DB_NAME=$$(grep TEST_DB_NAME .env | cut -d '=' -f2); \
	DB_USER=$$(grep TEST_DB_USER .env | cut -d '=' -f2); \
	env $$(grep ^TEST_ .env | sed 's/^TEST_//') docker-compose exec db psql -U $$DB_USER -c "DROP DATABASE IF EXISTS $$DB_NAME;"

lint:
	@echo "🧼 Running linters in Docker container..."
	docker-compose exec web black . --line-length=120
	docker-compose exec web isort . --profile=black --line-length=120
	docker-compose exec web flake8 .
	docker-compose exec web mypy . --ignore-missing-imports --disallow-untyped-defs
