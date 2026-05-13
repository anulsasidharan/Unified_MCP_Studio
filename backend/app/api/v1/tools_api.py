import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.project import Project
from app.models.tool import Tool
from app.models.user import User
from app.schemas.tool import ToolCreate, ToolPublic, ToolUpdate

router = APIRouter(tags=["tools"])


def _not_found() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error": {"code": "NOT_FOUND", "message": "Tool not found", "details": {}}},
    )


async def _get_project(
    db: AsyncSession, project_id: uuid.UUID, user_id: uuid.UUID
) -> Project:
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if project is None or project.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "NOT_FOUND", "message": "Project not found", "details": {}}},
        )
    return project


async def _get_tool_owned(
    db: AsyncSession, tool_id: uuid.UUID, user_id: uuid.UUID
) -> Tool:
    result = await db.execute(select(Tool).where(Tool.id == tool_id))
    tool = result.scalar_one_or_none()
    if tool is None:
        raise _not_found()
    await _get_project(db, tool.project_id, user_id)
    return tool


@router.get("/projects/{project_id}/tools", response_model=list[ToolPublic])
async def list_tools(
    project_id: uuid.UUID,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[Tool]:
    await _get_project(db, project_id, current.id)
    result = await db.execute(
        select(Tool).where(Tool.project_id == project_id).order_by(Tool.created_at)
    )
    return list(result.scalars().all())


@router.post(
    "/projects/{project_id}/tools", response_model=ToolPublic, status_code=status.HTTP_201_CREATED
)
async def create_tool(
    project_id: uuid.UUID,
    body: ToolCreate,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Tool:
    await _get_project(db, project_id, current.id)
    tool = Tool(
        project_id=project_id,
        name=body.name,
        description=body.description,
        input_schema=body.input_schema,
        handler_code=body.handler_code,
        handler_language=body.handler_language,
        tool_metadata={},
    )
    db.add(tool)
    await db.commit()
    await db.refresh(tool)
    return tool


@router.get("/tools/{tool_id}", response_model=ToolPublic)
async def get_tool(
    tool_id: uuid.UUID,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Tool:
    return await _get_tool_owned(db, tool_id, current.id)


@router.put("/tools/{tool_id}", response_model=ToolPublic)
async def update_tool(
    tool_id: uuid.UUID,
    body: ToolUpdate,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Tool:
    tool = await _get_tool_owned(db, tool_id, current.id)
    if body.name is not None:
        tool.name = body.name
    if body.description is not None:
        tool.description = body.description
    if body.input_schema is not None:
        tool.input_schema = body.input_schema
    if body.handler_code is not None:
        tool.handler_code = body.handler_code
    if body.handler_language is not None:
        tool.handler_language = body.handler_language
    await db.commit()
    await db.refresh(tool)
    return tool


@router.delete("/tools/{tool_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tool(
    tool_id: uuid.UUID,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    tool = await _get_tool_owned(db, tool_id, current.id)
    await db.delete(tool)
    await db.commit()
