"""Ownership helpers — scope rows to authenticated users."""

import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.prompt import Prompt
from app.models.resource import Resource
from app.models.tool import Tool
from app.models.user import User


async def require_project(
    db: AsyncSession,
    user: User,
    project_id: uuid.UUID,
) -> Project:
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.user_id == user.id),
    )
    project = result.scalar_one_or_none()
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "PROJECT_NOT_FOUND",
                    "message": "Project not found",
                    "details": {},
                }
            },
        )
    return project


async def require_tool(db: AsyncSession, user: User, tool_id: uuid.UUID) -> Tool:
    result = await db.execute(
        select(Tool)
        .join(Project, Tool.project_id == Project.id)
        .where(Tool.id == tool_id, Project.user_id == user.id),
    )
    tool = result.scalar_one_or_none()
    if tool is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "TOOL_NOT_FOUND",
                    "message": "Tool not found",
                    "details": {},
                }
            },
        )
    return tool


async def require_resource(db: AsyncSession, user: User, resource_id: uuid.UUID) -> Resource:
    result = await db.execute(
        select(Resource)
        .join(Project, Resource.project_id == Project.id)
        .where(Resource.id == resource_id, Project.user_id == user.id),
    )
    row = result.scalar_one_or_none()
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "RESOURCE_NOT_FOUND",
                    "message": "Resource not found",
                    "details": {},
                }
            },
        )
    return row


async def require_prompt(db: AsyncSession, user: User, prompt_id: uuid.UUID) -> Prompt:
    result = await db.execute(
        select(Prompt)
        .join(Project, Prompt.project_id == Project.id)
        .where(Prompt.id == prompt_id, Project.user_id == user.id),
    )
    row = result.scalar_one_or_none()
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "PROMPT_NOT_FOUND",
                    "message": "Prompt not found",
                    "details": {},
                }
            },
        )
    return row
