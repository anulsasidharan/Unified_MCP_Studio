# MCP server codegen templates (Jinja2)

This directory holds **Jinja2** templates for generated **TypeScript** and **Python** MCP servers (stdio by default), per `docs/PRD.md` and Phase 4 in `TASKS.md`.

| Subfolder     | Purpose                          |
|---------------|----------------------------------|
| `typescript/` | TS MCP SDK server skeleton       |
| `python/`     | Python MCP server skeleton       |

Application-owned template packs used by the backend codegen service will be added in later phases. Repo `backend/app/core/templates/` (if introduced) is for **API/runtime** helpers only; **authoritative server templates** live here at the monorepo root.
