# Unified MCP Studio

Visual development environment for **Model Context Protocol (MCP)** servers. See **`docs/PRD.md`**, **`docs/ARCHITECTURE.md`**, and **`TASKS.md`** for scope and phases.

## Repository layout (Phase 0)

| Path | Role |
|------|------|
| `frontend/` | Next.js 14 (App Router) — studio UI |
| `backend/` | FastAPI — `/api/v1` REST API |
| `templates/` | Jinja2 packs for generated MCP servers (Phase 4+) |
| `docker-compose.yml` | Local **PostgreSQL 15** and **Redis 7** |

## Quick start

1. **Data services** (from repo root):

   ```bash
   docker compose up -d postgres redis
   ```

2. **API** (`backend/README.md`):

   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate
   pip install -e ".[dev]"
   copy .env.example .env
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   - `GET http://localhost:8000/health`
   - `GET http://localhost:8000/api/v1/health`

3. **Web** (`frontend/README.md`):

   ```bash
   cd frontend
   npm install
   copy .env.example .env.local
   npm run dev
   ```

Optional: `make dev-up` starts Postgres and Redis.

## Product docs

- `docs/API_SPEC.md` — HTTP contract (`/api/v1`)
- `docs/DB_SCHEMA.md` — persistence model
- `docs/DEPLOYMENT.md` — GCP-oriented operations
