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
	ENV_FILE=$(ENV_FILE) docker-compose up -d --build

test:
	@WEB_NAME=$$(docker ps --format '{{.Names}}' | grep web-1); \
	DB_NAME=$$(docker ps --format '{{.Names}}' | grep db-1); \
	if [ -z "$$DB_NAME" ]; then echo "Postgres container not found!"; exit 1; fi; \
	if [ -z "$$WEB_NAME" ]; then echo "Web container not found!"; exit 1; fi; \
	echo "Dropping + creating user and DB in $$DB_NAME..."; \
	docker exec -i $$DB_NAME psql -U postgres -c "DROP USER IF EXISTS app_db_user; CREATE USER app_db_user WITH PASSWORD 'SECRET_PASS'; ALTER ROLE app_db_user WITH CREATEDB;"; \
	docker exec -i $$DB_NAME psql -U app_db_user -c "DROP DATABASE IF EXISTS app_db_user; CREATE DATABASE app_db_user; GRANT ALL PRIVILEGES ON DATABASE app_db_user TO app_db_user;"; \
	echo "🚀 Running tests in $$WEB_NAME..."; \
	docker exec -it $$WEB_NAME pytest -s






