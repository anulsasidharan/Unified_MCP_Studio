"""Sandbox testing endpoints."""

import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.project import Project
from app.models.tool import Tool
from app.models.user import User

router = APIRouter(prefix="/testing", tags=["testing"])

_sessions: dict[str, uuid.UUID] = {}


class SandboxStartRequest(BaseModel):
    project_id: str


class SandboxStartResponse(BaseModel):
    session_id: str


class SandboxExecuteRequest(BaseModel):
    session_id: str
    tool_name: str
    arguments: dict[str, Any] = {}


class SandboxExecuteResponse(BaseModel):
    ok: bool
    stdout: str
    stderr: str
    detail: str | None


@router.post("/sandbox/start", response_model=SandboxStartResponse)
async def start_sandbox(
    body: SandboxStartRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SandboxStartResponse:
    result = await db.execute(
        select(Project).where(
            Project.id == body.project_id,
            Project.user_id == current_user.id,
        )
    )
    project = result.scalar_one_or_none()
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "NOT_FOUND", "message": "Project not found", "details": {}}},
        )
    session_id = str(uuid.uuid4())
    _sessions[session_id] = uuid.UUID(str(body.project_id))
    return SandboxStartResponse(session_id=session_id)


@router.post("/sandbox/execute", response_model=SandboxExecuteResponse)
async def execute_sandbox(
    body: SandboxExecuteRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SandboxExecuteResponse:
    project_id = _sessions.get(body.session_id)
    if project_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": {"code": "INVALID_SESSION", "message": "Session not found. Start a sandbox first.", "details": {}}},
        )
    result = await db.execute(
        select(Tool).join(Project).where(
            Project.id == project_id,
            Project.user_id == current_user.id,
            Tool.name == body.tool_name,
        )
    )
    tool = result.scalar_one_or_none()
    if tool is None:
        return SandboxExecuteResponse(
            ok=False,
            stdout="",
            stderr=f"Tool '{body.tool_name}' not found in project.",
            detail="Tool not found",
        )
    return SandboxExecuteResponse(
        ok=True,
        stdout=f"Tool '{body.tool_name}' invoked with args: {body.arguments}\n[Sandbox execution requires Docker — see docs/SANDBOX.md]",
        stderr="",
        detail=None,
    )


@router.post("/sandbox/stop", status_code=status.HTTP_204_NO_CONTENT)
async def stop_sandbox(
    body: SandboxStartRequest,
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    pass


@router.get("/results/{result_id}")
async def get_result(
    result_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict[str, Any]:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error": {"code": "NOT_FOUND", "message": "Result not found", "details": {}}},
    )
