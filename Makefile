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
	docker-compose exec web alembic revision --autogenerate

migrate:
	docker-compose exec web alembic upgrade head

test:
	docker-compose exec web pytest -s

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pip install pre-commit

lint:
	pre-commit run --all-files
