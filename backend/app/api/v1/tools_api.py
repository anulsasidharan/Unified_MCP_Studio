"""Tools nested under projects + `/tools/{id}` (docs/API_SPEC.md §4)."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.tool import Tool
from app.models.user import User
from app.schemas.tool import ToolCreate, ToolRead, ToolTestRequest, ToolTestResponse, ToolUpdate
from app.services.access import require_project, require_tool
from app.services.validation_service import validate_payload_against_tool_schema

proj_router = APIRouter(prefix="/projects/{project_id}/tools", tags=["tools"])
id_router = APIRouter(prefix="/tools", tags=["tools"])


@proj_router.get("", response_model=list[ToolRead])
async def list_tools(
    project_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> list[Tool]:
    await require_project(db, user, project_id)
    result = await db.execute(select(Tool).where(Tool.project_id == project_id))
    return list(result.scalars().all())


@proj_router.post("", response_model=ToolRead, status_code=status.HTTP_201_CREATED)
async def create_tool(
    project_id: uuid.UUID,
    body: ToolCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Tool:
    await require_project(db, user, project_id)
    tool = Tool(
        project_id=project_id,
        name=body.name,
        description=body.description,
        input_schema=body.input_schema,
        handler_code=body.handler_code,
        handler_language=body.handler_language,
        metadata_=body.metadata or {},
    )
    db.add(tool)
    await db.commit()
    await db.refresh(tool)
    return tool


@id_router.get("/{tool_id}", response_model=ToolRead)
async def get_tool(
    tool_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Tool:
    return await require_tool(db, user, tool_id)


@id_router.put("/{tool_id}", response_model=ToolRead)
async def update_tool(
    tool_id: uuid.UUID,
    body: ToolUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Tool:
    tool = await require_tool(db, user, tool_id)
    data = body.model_dump(exclude_unset=True)
    if "metadata" in data:
        data["metadata_"] = data.pop("metadata")
    for k, v in data.items():
        setattr(tool, k, v)
    await db.commit()
    await db.refresh(tool)
    return tool


@id_router.delete("/{tool_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tool(
    tool_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> None:
    tool = await require_tool(db, user, tool_id)
    await db.delete(tool)
    await db.commit()


@id_router.post("/{tool_id}/test", response_model=ToolTestResponse)
async def test_tool(
    tool_id: uuid.UUID,
    body: ToolTestRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> ToolTestResponse:
    tool = await require_tool(db, user, tool_id)
    try:
        validate_payload_against_tool_schema(tool.input_schema, body.arguments)
    except Exception as exc:
        return ToolTestResponse(ok=False, detail=str(exc))
    return ToolTestResponse(ok=True, result={"validated": True}, detail=None)
