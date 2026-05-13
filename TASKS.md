# Unified MCP Studio — Development phases & feature branches

**Conventions:** one **`feature/<branch-name>`** branch per sub-task; merge via PR to `main`. Order reduces rework: **auth & schema** before **designer**; **codegen** before **sandbox**; **sandbox** before **deploy**.

---

## Phase 0 — Repository & docs baseline

| Sub-task | Feature branch |
|----------|----------------|
| Monorepo scaffold (`frontend/`, `backend/`, `templates/`, compose) | `feature/scaffold-monorepo` |
| Align `CLAUDE.md` with implemented paths | `feature/docs-claude-sync` |
| Backend `config.py` + `.env.example` + health route | `feature/backend-config-health` |

---

## Phase 1 — Auth & users

| Sub-task | Feature branch |
|----------|----------------|
| Users model + Alembic initial migration | `feature/db-users-migration` |
| Register / login / me (`/api/v1/auth/*`) | `feature/api-auth-jwt` |
| Next.js auth pages + token storage | `feature/frontend-auth-flow` |

---

## Phase 2 — Projects CRUD

| Sub-task | Feature branch |
|----------|----------------|
| `projects` table + API CRUD | `feature/api-projects-crud` |
| Studio project list & detail pages | `feature/frontend-projects-ui` |

---

## Phase 3 — Tools, resources, prompts

| Sub-task | Feature branch |
|----------|----------------|
| ORM + API for tools | `feature/api-tools-crud` |
| ORM + API for resources | `feature/api-resources-crud` |
| ORM + API for prompts | `feature/api-prompts-crud` |
| Designer UI: React Flow nodes + forms | `feature/frontend-designer-mvp` |
| JSON Schema validation service | `feature/backend-jsonschema-validate` |

---

## Phase 4 — Code generation

| Sub-task | Feature branch |
|----------|----------------|
| Jinja2 template pack (TS + Python minimal server) | `feature/codegen-jinja-templates` |
| `POST /projects/{id}/validate` + `generate` + Celery `codegen` queue | `feature/backend-codegen-pipeline` |
| GCS upload + `download` signed URL | `feature/backend-artifact-gcs` |

---

## Phase 5 — Sandbox & testing console

| Sub-task | Feature branch |
|----------|----------------|
| Celery `sandbox` queue + worker subprocess wrapper | `feature/backend-sandbox-worker` |
| `testing/sandbox/*` API + resource limits | `feature/api-sandbox-lifecycle` |
| Frontend testing console (invoke tool, show logs) | `feature/frontend-testing-console` |
| Optional: Claude-backed tool test | `feature/backend-claude-test-proxy` |

---

## Phase 6 — Templates

| Sub-task | Feature branch |
|----------|----------------|
| `templates` seed data + list/get API | `feature/api-templates-library` |
| `POST /projects/from-template` | `feature/backend-instantiate-template` |
| Template gallery UI | `feature/frontend-template-gallery` |

---

## Phase 7 — Deployments (MVP+)

| Sub-task | Feature branch |
|----------|----------------|
| `deployments` model + status API | `feature/api-deployments-crud` |
| Cloud Run deploy job (skaffold or gcloud from worker) | `feature/worker-cloud-run-deploy` |

---

## Phase 8 — GCP hardening

| Sub-task | Feature branch |
|----------|----------------|
| Terraform or Deployment Manager baseline (VPC, SQL, Redis, GCS) | `feature/infra-gcp-baseline` |
| GitHub Actions OIDC → deploy Cloud Run | `feature/ci-gcp-oidc-deploy` |
| Cloud Armor + budgets (optional) | `feature/infra-gcp-security-cost` |

---

## Dependency summary

1. Phase 0 before all.  
2. Phase 1 → 2 → 3 in order for permissioned CRUD.  
3. Phase 4 after tool/resource/prompt persistence exists.  
4. Phase 5 after codegen produces runnable tree.  
5. Phase 6 can overlap late Phase 3–4 once project shape stable.  
6. Phase 7–8 after a working API image and secrets story.

---

## Optional follow-ups

| Sub-task | Feature branch |
|----------|----------------|
| tRPC or OpenAPI client codegen for frontend | `feature/frontend-api-client-trpc` |
| SSE transport + hosted MCP URL | `feature/backend-mcp-sse-transport` |
