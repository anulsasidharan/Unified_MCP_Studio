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
