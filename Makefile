# Optional dev shortcuts (docs/ARCHITECTURE.md).
.PHONY: dev-up dev-down backend-install frontend-install db-migrate

dev-up:
	docker compose up -d postgres redis

dev-down:
	docker compose down

backend-install:
	cd backend && python -m pip install -e ".[dev]"

frontend-install:
	cd frontend && npm install

db-migrate:
	cd backend && alembic upgrade head
