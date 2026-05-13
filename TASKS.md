# Unified MCP Studio — Development phases & feature branches

**Conventions:** one **`feature/<branch-name>`** branch per sub-task; merge via PR to `main`. Order reduces rework: **auth & schema** before **designer**; **codegen** before **sandbox**; **sandbox** before **deploy**.

**Tracking:** **SI No.** is a single running index across all sub-tasks below (1…n). When a sub-task is finished and merged, set **Status** to **`Completed ✅`**; otherwise **`Pending`**.

---

## Phase 0 — Repository & docs baseline

| SI No. | Sub-task | Feature branch | Status |
|--------|----------|----------------|--------|
| 1 | Monorepo scaffold (`frontend/`, `backend/`, `templates/`, compose) | `feature/scaffold-monorepo` | Completed ✅ |
| 2 | Align `CLAUDE.md` with implemented paths | `feature/docs-claude-sync` | Completed ✅ |
| 3 | Backend `config.py` + `.env.example` + health route | `feature/backend-config-health` | Completed ✅ |

---

## Phase 1 — Auth & users

| SI No. | Sub-task | Feature branch | Status |
|--------|----------|----------------|--------|
| 4 | Users model + Alembic initial migration | `feature/db-users-migration` | Completed ✅ |
| 5 | Register / login / me (`/api/v1/auth/*`) | `feature/api-auth-jwt` | Completed ✅ |
| 6 | Next.js auth pages + token storage | `feature/frontend-auth-flow` | Completed ✅ |

---

## Phase 2 — Projects CRUD

| SI No. | Sub-task | Feature branch | Status |
|--------|----------|----------------|--------|
| 7 | `projects` table + API CRUD | `feature/api-projects-crud` | Pending |
| 8 | Studio project list & detail pages | `feature/frontend-projects-ui` | Pending |

---

## Phase 3 — Tools, resources, prompts

| SI No. | Sub-task | Feature branch | Status |
|--------|----------|----------------|--------|
| 9 | ORM + API for tools | `feature/api-tools-crud` | Pending |
| 10 | ORM + API for resources | `feature/api-resources-crud` | Pending |
| 11 | ORM + API for prompts | `feature/api-prompts-crud` | Pending |
| 12 | Designer UI: React Flow nodes + forms | `feature/frontend-designer-mvp` | Pending |
| 13 | JSON Schema validation service | `feature/backend-jsonschema-validate` | Pending |

---

## Phase 4 — Code generation

| SI No. | Sub-task | Feature branch | Status |
|--------|----------|----------------|--------|
| 14 | Jinja2 template pack (TS + Python minimal server) | `feature/codegen-jinja-templates` | Pending |
| 15 | `POST /projects/{id}/validate` + `generate` + Celery `codegen` queue | `feature/backend-codegen-pipeline` | Pending |
| 16 | GCS upload + `download` signed URL | `feature/backend-artifact-gcs` | Pending |

---

## Phase 5 — Sandbox & testing console

| SI No. | Sub-task | Feature branch | Status |
|--------|----------|----------------|--------|
| 17 | Celery `sandbox` queue + worker subprocess wrapper | `feature/backend-sandbox-worker` | Pending |
| 18 | `testing/sandbox/*` API + resource limits | `feature/api-sandbox-lifecycle` | Pending |
| 19 | Frontend testing console (invoke tool, show logs) | `feature/frontend-testing-console` | Pending |
| 20 | Optional: Claude-backed tool test | `feature/backend-claude-test-proxy` | Pending |

---

## Phase 6 — Templates

| SI No. | Sub-task | Feature branch | Status |
|--------|----------|----------------|--------|
| 21 | `templates` seed data + list/get API | `feature/api-templates-library` | Pending |
| 22 | `POST /projects/from-template` | `feature/backend-instantiate-template` | Pending |
| 23 | Template gallery UI | `feature/frontend-template-gallery` | Pending |

---

## Phase 7 — Deployments (MVP+)

| SI No. | Sub-task | Feature branch | Status |
|--------|----------|----------------|--------|
| 24 | `deployments` model + status API | `feature/api-deployments-crud` | Pending |
| 25 | Cloud Run deploy job (skaffold or gcloud from worker) | `feature/worker-cloud-run-deploy` | Pending |

---

## Phase 8 — GCP hardening

| SI No. | Sub-task | Feature branch | Status |
|--------|----------|----------------|--------|
| 26 | Terraform or Deployment Manager baseline (VPC, SQL, Redis, GCS) | `feature/infra-gcp-baseline` | Pending |
| 27 | GitHub Actions OIDC → deploy Cloud Run | `feature/ci-gcp-oidc-deploy` | Pending |
| 28 | Cloud Armor + budgets (optional) | `feature/infra-gcp-security-cost` | Pending |

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

| SI No. | Sub-task | Feature branch | Status |
|--------|----------|----------------|--------|
| 29 | tRPC or OpenAPI client codegen for frontend | `feature/frontend-api-client-trpc` | Pending |
| 30 | SSE transport + hosted MCP URL | `feature/backend-mcp-sse-transport` | Pending |
