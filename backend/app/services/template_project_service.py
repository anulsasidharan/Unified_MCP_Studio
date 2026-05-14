"""Instantiate a new project from a library_templates.config snapshot."""

from __future__ import annotations

import uuid
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.library_template import LibraryTemplate
from app.models.project import Project
from app.models.prompt import Prompt
from app.models.resource import Resource
from app.models.tool import Tool


def _not_found() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error": {"code": "NOT_FOUND", "message": "Template not found", "details": {}}},
    )


def _bad_template(msg: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={
            "error": {
                "code": "INVALID_TEMPLATE_CONFIG",
                "message": msg,
                "details": {},
            }
        },
    )


def _require_str(d: dict[str, Any], key: str, ctx: str) -> str:
    v = d.get(key)
    if not isinstance(v, str) or not v.strip():
        raise _bad_template(f"{ctx}: missing or invalid string field {key!r}")
    return v.strip()


def _optional_str(d: dict[str, Any], key: str) -> str | None:
    v = d.get(key)
    if v is None:
        return None
    if not isinstance(v, str):
        raise _bad_template(f"expected string or null for {key!r}")
    return v or None


def _parse_tools(raw: Any) -> list[dict[str, Any]]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise _bad_template("config.tools must be an array when present")
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            raise _bad_template(f"config.tools[{i}] must be an object")
        name = _require_str(item, "name", f"tools[{i}]")
        if name in seen:
            raise _bad_template(f"duplicate tool name {name!r}")
        seen.add(name)
        desc = _optional_str(item, "description")
        schema = item.get("input_schema")
        if not isinstance(schema, dict):
            raise _bad_template(f"tools[{i}].input_schema must be an object")
        handler = _require_str(item, "handler_code", f"tools[{i}]")
        lang = _require_str(item, "handler_language", f"tools[{i}]")
        meta = item.get("metadata")
        if meta is None:
            meta = {}
        elif not isinstance(meta, dict):
            raise _bad_template(f"tools[{i}].metadata must be an object when present")
        out.append(
            {
                "name": name[:255],
                "description": desc,
                "input_schema": schema,
                "handler_code": handler,
                "handler_language": lang[:50],
                "metadata": meta,
            }
        )
    return out


def _parse_resources(raw: Any) -> list[dict[str, Any]]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise _bad_template("config.resources must be an array when present")
    out: list[dict[str, Any]] = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            raise _bad_template(f"config.resources[{i}] must be an object")
        uri = _require_str(item, "uri", f"resources[{i}]")[:500]
        name = _require_str(item, "name", f"resources[{i}]")[:255]
        code = _require_str(item, "provider_code", f"resources[{i}]")
        out.append(
            {
                "uri": uri,
                "name": name,
                "description": _optional_str(item, "description"),
                "mime_type": _optional_str(item, "mime_type"),
                "provider_code": code,
            }
        )
    return out


def _parse_prompts(raw: Any) -> list[dict[str, Any]]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise _bad_template("config.prompts must be an array when present")
    out: list[dict[str, Any]] = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            raise _bad_template(f"config.prompts[{i}] must be an object")
        name = _require_str(item, "name", f"prompts[{i}]")[:255]
        args = item.get("arguments", [])
        msgs = item.get("messages", [])
        if not isinstance(args, list):
            raise _bad_template(f"prompts[{i}].arguments must be an array")
        if not isinstance(msgs, list):
            raise _bad_template(f"prompts[{i}].messages must be an array")
        out.append(
            {
                "name": name,
                "description": _optional_str(item, "description"),
                "arguments": args,
                "messages": msgs,
            }
        )
    return out


async def create_project_from_library_template(
    db: AsyncSession,
    *,
    user_id: uuid.UUID,
    template_id: uuid.UUID,
    project_name: str | None,
) -> Project:
    result = await db.execute(select(LibraryTemplate).where(LibraryTemplate.id == template_id))
    template = result.scalar_one_or_none()
    if template is None:
        raise _not_found()
    if not template.is_public and template.author_id != user_id:
        raise _not_found()

    cfg = template.config
    if not isinstance(cfg, dict):
        raise _bad_template("template.config must be a JSON object")

    runtime = cfg.get("runtime")
    if not isinstance(runtime, str) or not runtime.strip():
        raise _bad_template("template.config.runtime is required")
    transport = cfg.get("transport")
    if not isinstance(transport, str) or not transport.strip():
        raise _bad_template("template.config.transport is required")

    tools = _parse_tools(cfg.get("tools"))
    resources = _parse_resources(cfg.get("resources"))
    prompts = _parse_prompts(cfg.get("prompts"))

    name = (project_name or template.name).strip()[:255]
    if not name:
        raise _bad_template("project name cannot be empty")

    project = Project(
        user_id=user_id,
        name=name,
        description=template.description,
        runtime=runtime.strip()[:50],
        transport=transport.strip()[:50],
        config={"source_template_id": str(template.id)},
    )
    db.add(project)
    await db.flush()

    for t in tools:
        db.add(
            Tool(
                project_id=project.id,
                name=t["name"],
                description=t["description"],
                input_schema=t["input_schema"],
                handler_code=t["handler_code"],
                handler_language=t["handler_language"],
                tool_metadata=t["metadata"],
            )
        )
    for r in resources:
        db.add(
            Resource(
                project_id=project.id,
                uri=r["uri"],
                name=r["name"],
                description=r["description"],
                mime_type=r["mime_type"],
                provider_code=r["provider_code"],
            )
        )
    for p in prompts:
        db.add(
            Prompt(
                project_id=project.id,
                name=p["name"],
                description=p["description"],
                arguments=p["arguments"],
                messages=p["messages"],
            )
        )

    template.use_count = int(template.use_count) + 1
    await db.commit()
    await db.refresh(project)
    return project
