# Unified MCP Studio — Web

Next.js 14 (App Router) under `src/app/`, aligned with `docs/ARCHITECTURE.md`.

## Local run

```bash
npm install
copy .env.example .env.local
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). Point `NEXT_PUBLIC_API_BASE_URL` at the FastAPI server (default `http://localhost:8000`).
