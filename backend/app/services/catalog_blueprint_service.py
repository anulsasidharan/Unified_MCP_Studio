"""Create projects from built-in catalog JSON or validated blueprint exports."""

from __future__ import annotations

import json
import re
import uuid
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.tool import Tool

_CATALOG_PATH = Path(__file__).resolve().parent.parent / "data" / "mcp_template_catalog.json"


def _not_found() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "error": {
                "code": "NOT_FOUND",
                "message": "Catalog blueprint not found",
                "details": {},
            }
        },
    )


def _catalog_unavailable() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail={
            "error": {
                "code": "CATALOG_UNAVAILABLE",
                "message": "MCP template catalog file is missing on the server.",
                "details": {},
            }
        },
    )


def _invalid_blueprint(msg: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={
            "error": {
                "code": "INVALID_BLUEPRINT",
                "message": msg,
                "details": {},
            }
        },
    )


@lru_cache(maxsize=1)
def _blueprint_index() -> dict[str, dict[str, Any]]:
    if not _CATALOG_PATH.is_file():
        return {}
    raw = json.loads(_CATALOG_PATH.read_text(encoding="utf-8"))
    items = raw.get("blueprints") if isinstance(raw, dict) else raw
    if not isinstance(items, list):
        return {}
    out: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        bid = item.get("id")
        if isinstance(bid, str) and bid.strip():
            out[bid.strip()] = item
    return out


def get_catalog_blueprint(blueprint_id: str) -> dict[str, Any] | None:
    idx = _blueprint_index()
    if not idx:
        return None
    return idx.get(blueprint_id.strip())


def _sanitize_tool_name(raw: str, idx: int) -> str:
    base = re.sub(r"[^a-zA-Z0-9_]", "_", (raw or "").strip())
    if not base:
        base = f"tool_{idx}"
    if base[0].isdigit():
        base = f"t_{base}"
    return base[:255]


_STUB_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": True,
    "description": "Tool arguments (stub schema — refine in the designer).",
}


def _stub_handler_python(tool_name: str, blueprint_id: str) -> str:
    return (
        "# Catalog blueprint stub — implement using the project description or an imported JSON export.\n"
        f"TOOL_NAME = {tool_name!r}\n"
        f"BLUEPRINT_ID = {blueprint_id!r}\n\n"
        "async def run(arguments: dict):\n"
        "    if not isinstance(arguments, dict):\n"
        "        arguments = {}\n"
        "    return {\n"
        "        'stub': True,\n"
        "        'tool': TOOL_NAME,\n"
        "        'blueprint_id': BLUEPRINT_ID,\n"
        "        'argument_keys': list(arguments.keys()),\n"
        "    }\n"
    )


def _stub_handler_typescript(tool_name: str, blueprint_id: str) -> str:
    return (
        "/** Catalog blueprint stub — implement in the designer. */\n"
        f"const TOOL_NAME = {json.dumps(tool_name)};\n"
        f"const BLUEPRINT_ID = {json.dumps(blueprint_id)};\n\n"
        "export default async function handle(args: Record<string, unknown>) {\n"
        "  const a = args && typeof args === 'object' ? args : {};\n"
        "  return {\n"
        "    stub: true,\n"
        "    tool: TOOL_NAME,\n"
        "    blueprintId: BLUEPRINT_ID,\n"
        "    argumentKeys: Object.keys(a as object),\n"
        "  };\n"
        "}\n"
    )


def _stub_handler(runtime: str, tool_name: str, blueprint_id: str) -> str:
    r = runtime.strip().lower()
    if r == "typescript":
        return _stub_handler_typescript(tool_name, blueprint_id)
    return _stub_handler_python(tool_name, blueprint_id)


def _tool_language(runtime: str) -> str:
    return "typescript" if runtime.strip().lower() == "typescript" else "python"


def _parse_suggested_tools(bp: dict[str, Any]) -> list[str]:
    raw = bp.get("suggestedTools")
    if not isinstance(raw, list) or not raw:
        raise _invalid_blueprint("blueprint.suggestedTools must be a non-empty array")
    names: list[str] = []
    for i, item in enumerate(raw):
        if not isinstance(item, str) or not item.strip():
            raise _invalid_blueprint(f"blueprint.suggestedTools[{i}] must be a non-empty string")
        names.append(item.strip())
    return names


async def create_project_from_blueprint_dict(
    db: AsyncSession,
    *,
    user_id: uuid.UUID,
    blueprint: dict[str, Any],
    project_name: str | None,
) -> Project:
    bid = blueprint.get("id")
    if not isinstance(bid, str) or not bid.strip():
        raise _invalid_blueprint("blueprint.id is required")

    runtime = blueprint.get("primaryRuntime")
    transport = blueprint.get("transport")
    if not isinstance(runtime, str) or not runtime.strip():
        raise _invalid_blueprint("blueprint.primaryRuntime is required")
    if not isinstance(transport, str) or not transport.strip():
        raise _invalid_blueprint("blueprint.transport is required")
    rts = runtime.strip().lower()
    if rts not in ("typescript", "python"):
        raise _invalid_blueprint("blueprint.primaryRuntime must be 'typescript' or 'python'")
    trs = transport.strip().lower()
    if trs not in ("stdio", "sse"):
        raise _invalid_blueprint("blueprint.transport must be 'stdio' or 'sse'")

    tier = blueprint.get("tier")
    tier_s = tier.strip() if isinstance(tier, str) else ""

    title = blueprint.get("name")
    default_name = title.strip() if isinstance(title, str) and title.strip() else "Untitled project"
    name = (project_name or default_name).strip()[:255]
    if not name:
        raise _invalid_blueprint("project name cannot be empty")

    tagline = blueprint.get("tagline") if isinstance(blueprint.get("tagline"), str) else ""
    overview = blueprint.get("overview") if isinstance(blueprint.get("overview"), str) else ""
    design = blueprint.get("design") if isinstance(blueprint.get("design"), str) else ""
    ext = blueprint.get("extensionIdeas") if isinstance(blueprint.get("extensionIdeas"), str) else ""
    risks = blueprint.get("risks") if isinstance(blueprint.get("risks"), str) else ""

    description = "\n\n".join(
        p for p in (tagline, overview, design, ext, risks) if p
    )[:20000] or None

    tool_names = _parse_suggested_tools(blueprint)
    seen: set[str] = set()
    resolved: list[str] = []
    for i, tn in enumerate(tool_names):
        base = _sanitize_tool_name(tn, i)
        final = base
        n = 2
        while final in seen:
            suffix = f"_{n}"
            final = (base[: 255 - len(suffix)] + suffix)[:255]
            n += 1
        seen.add(final)
        resolved.append(final)

    project = Project(
        user_id=user_id,
        name=name,
        description=description,
        runtime=rts[:50],
        transport=trs[:50],
        config={
            "source_catalog_blueprint_id": bid.strip(),
            "catalog_tier": tier_s or None,
        },
    )
    db.add(project)
    await db.flush()

    lang = _tool_language(rts)
    for display_name, safe_name in zip(tool_names, resolved, strict=True):
        desc = f"Stub for `{display_name}` — from catalog blueprint `{bid}`. Replace handler per design notes."
        handler = _stub_handler(rts, display_name, bid.strip())
        db.add(
            Tool(
                project_id=project.id,
                name=safe_name,
                description=desc[:2000],
                input_schema=_STUB_SCHEMA,
                handler_code=handler,
                handler_language=lang,
                tool_metadata={"catalog_tool_label": display_name, "blueprint_id": bid.strip()},
            )
        )

    await db.commit()
    await db.refresh(project)
    return project


async def create_project_from_catalog_blueprint_id(
    db: AsyncSession,
    *,
    user_id: uuid.UUID,
    blueprint_id: str,
    project_name: str | None,
) -> Project:
    idx = _blueprint_index()
    if not idx:
        raise _catalog_unavailable()
    bp = idx.get(blueprint_id.strip())
    if bp is None:
        raise _not_found()
    return await create_project_from_blueprint_dict(
        db, user_id=user_id, blueprint=bp, project_name=project_name
    )
