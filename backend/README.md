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

### PostgreSQL connection errors (`DATABASE_UNAVAILABLE`)

The API returns this when it cannot open a DB session (wrong host, port down, bad password, or Postgres not running).

1. **Start Postgres** (from repo root, not `backend/`):  
   `docker compose up -d postgres`  
   Wait until `docker compose ps` shows `postgres` as **healthy** (Alembic and auth need a live server).

2. **Match where the API runs to the hostname in `DATABASE_URL`**

   | API process | `DATABASE_URL` host | Port |
   |-------------|---------------------|------|
   | `uvicorn` on your machine (Windows/macOS/Linux) | `127.0.0.1` | Host-mapped port, usually `5432`, or `POSTGRES_PORT` if you set it in the same `.env` file Docker Compose reads |
   | `backend` service in `docker compose` | `postgres` | `5432` (internal) |

   Copy `backend/.env.example` to `backend/.env`. For local uvicorn the default  
   `postgresql+asyncpg://mcpstudio:mcpstudio@127.0.0.1:5432/mcpstudio`  
   matches `docker-compose.yml` defaults (`POSTGRES_*`).

3. **Credentials** must match `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` in compose. If you changed the password after data was created, Postgres may still use the old password in the volume; either restore the old password in `DATABASE_URL` or reset the volume: `docker compose down -v` (deletes local DB data).

4. **Run migrations** once Postgres is up: from `backend/`, `alembic upgrade head`.

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
