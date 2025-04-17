ENV_FILE ?= .env

up:
	ENV_FILE=$(ENV_FILE) docker-compose up -d --build

down:
	docker-compose down

run:
	ENV_FILE=$(ENV_FILE) docker-compose up -d --build
	docker-compose exec web bash

migrate:
	docker-compose exec web alembic upgrade head

makemigrations:
	docker-compose exec web alembic revision --autogenerate -m "$(name)"

rebuild:
	docker-compose down --volumes --remove-orphans
	ENV_FILE=$(ENV_FILE) docker-compose up --build

test:
	DB_NAME=$(shell grep TEST_DB_NAME .env | cut -d '=' -f2); \
	DB_USER=$(shell grep TEST_DB_USER .env | cut -d '=' -f2); \
	env $$(grep ^TEST_ .env | sed 's/^TEST_//') docker-compose exec db psql -U $$DB_USER -tc "SELECT 1 FROM pg_database WHERE datname='$$DB_NAME'" | grep -q 1 || \
	env $$(grep ^TEST_ .env | sed 's/^TEST_//') docker-compose exec db psql -U $$DB_USER -c "CREATE DATABASE $$DB_NAME;"; \
	env $$(grep ^TEST_ .env | sed 's/^TEST_//') docker-compose exec db psql -U $$DB_USER -d $$DB_NAME -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL PRIVILEGES ON SCHEMA public TO $$DB_USER;"
	env $$(grep ^TEST_ .env | sed 's/^TEST_//') docker-compose exec web pytest -s -v



