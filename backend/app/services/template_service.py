"""Library templates — list/get/instantiate (Phase 6)."""

from __future__ import annotations

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.library_template import LibraryTemplate
from app.models.project import Project
from app.models.prompt import Prompt
from app.models.resource import Resource
from app.models.tool import Tool
from app.models.user import User


async def list_templates(
    db: AsyncSession,
    *,
    skip: int,
    limit: int,
) -> tuple[list[LibraryTemplate], int]:
    total = await db.scalar(select(func.count()).select_from(LibraryTemplate))
    result = await db.execute(
        select(LibraryTemplate).order_by(LibraryTemplate.name.asc()).offset(skip).limit(limit),
    )
    return list(result.scalars().all()), int(total or 0)


async def get_template(db: AsyncSession, template_id: uuid.UUID) -> LibraryTemplate | None:
    return await db.get(LibraryTemplate, template_id)


async def instantiate_template(db: AsyncSession, user: User, template_id: uuid.UUID) -> Project:
    tpl = await get_template(db, template_id)
    if tpl is None:
        raise ValueError("template not found")
    cfg = tpl.config or {}
    proj_meta = cfg.get("project") or {}
    runtime = cfg.get("runtime") or "python"
    transport = cfg.get("transport") or "stdio"

    project = Project(
        user_id=user.id,
        name=str(proj_meta.get("name") or tpl.name),
        description=proj_meta.get("description"),
        runtime=str(runtime),
        transport=str(transport),
        config={},
    )
    db.add(project)
    await db.flush()

    for t in cfg.get("tools") or []:
        db.add(
            Tool(
                project_id=project.id,
                name=str(t["name"]),
                description=t.get("description"),
                input_schema=t.get("input_schema") or {"type": "object"},
                handler_code=str(t.get("handler_code") or ""),
                handler_language=str(t.get("handler_language") or "python"),
                metadata_=t.get("metadata") or {},
            ),
        )
    for r in cfg.get("resources") or []:
        db.add(
            Resource(
                project_id=project.id,
                uri=str(r["uri"]),
                name=str(r["name"]),
                description=r.get("description"),
                mime_type=r.get("mime_type"),
                provider_code=str(r.get("provider_code") or ""),
            ),
        )
    for p in cfg.get("prompts") or []:
        db.add(
            Prompt(
                project_id=project.id,
                name=str(p["name"]),
                description=p.get("description"),
                arguments=p.get("arguments") or [],
                messages=p.get("messages") or [],
            ),
        )

    tpl.use_count = int(tpl.use_count or 0) + 1
    await db.commit()
    await db.refresh(project)
    return project
