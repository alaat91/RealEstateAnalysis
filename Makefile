.PHONY: install run test lint format migrate revision docker-up docker-down

install:
	pip install -e ".[dev]"

run:
	uvicorn app.main:app --reload

test:
	pytest -q

lint:
	ruff check app tests
	mypy app

format:
	ruff format app tests
	ruff check --fix app tests

migrate:
	alembic upgrade head

revision:
	alembic revision --autogenerate -m "$(m)"

docker-up:
	docker compose up --build

docker-down:
	docker compose down
