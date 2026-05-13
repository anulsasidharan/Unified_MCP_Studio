# Unified MCP Studio — API

FastAPI application (`app/` package). See root `docs/ARCHITECTURE.md` and `docs/API_SPEC.md`.

## Local run

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -e ".[dev]"
copy .env.example .env   # then edit
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Health (load balancers): `GET http://localhost:8000/health`
- Versioned health: `GET http://localhost:8000/api/v1/health`

Bring up Postgres and Redis from the repo root: `docker compose up -d postgres redis`.

## Database migrations (Alembic)

From `backend/` after Postgres is up and `.env` has `DATABASE_URL`:

```bash
alembic upgrade head
```

Create a new revision after model changes (review the generated file before applying):

```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

## Auth (Phase 1)

- `POST /api/v1/auth/register` — JSON body `{ "email", "password", "name?" }`
- `POST /api/v1/auth/login` — `{ "email", "password" }`
- `GET /api/v1/auth/me` — `Authorization: Bearer <access_token>`
- `POST /api/v1/auth/logout` — Bearer token; stateless JWT (client discards token)

Integration tests that hit Postgres: ensure `DATABASE_URL` / `TEST_DATABASE_URL` points at a running instance (see `tests/conftest.py`).
