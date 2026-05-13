"""Sandbox lifecycle + polling (docs/API_SPEC.md §9)."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.tool import Tool
from app.models.user import User
from app.schemas.sandbox import (
    SandboxExecuteRequest,
    SandboxExecuteResponse,
    SandboxStartRequest,
    SandboxStartResponse,
    SandboxStopRequest,
    TestResultsResponse,
)
from app.services import sandbox_service
from app.services.access import require_project

router = APIRouter(prefix="/testing", tags=["testing"])


@router.post("/sandbox/start", response_model=SandboxStartResponse)
async def sandbox_start(
    body: SandboxStartRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> SandboxStartResponse:
    await require_project(db, user, body.project_id)
    sess = await sandbox_service.start_session(db, body.project_id)
    return SandboxStartResponse(session_id=sess.session_id)


@router.post("/sandbox/execute", response_model=SandboxExecuteResponse)
async def sandbox_execute(
    body: SandboxExecuteRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> SandboxExecuteResponse:
    payload = sandbox_service.get_session_payload(body.session_id)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "SANDBOX_SESSION_NOT_FOUND",
                    "message": "Unknown sandbox session",
                    "details": {},
                }
            },
        )
    project_id = uuid.UUID(payload["project_id"])
    await require_project(db, user, project_id)
    result = await db.execute(
        select(Tool).where(Tool.project_id == project_id, Tool.name == body.tool_name),
    )
    tool = result.scalar_one_or_none()
    if tool is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {"code": "TOOL_NOT_FOUND", "message": "Tool not found", "details": {}},
            },
        )
    out = await sandbox_service.execute_tool(
        db,
        session_id=body.session_id,
        tool=tool,
        arguments=body.arguments,
    )
    return SandboxExecuteResponse(
        ok=bool(out.get("ok")),
        stdout=str(out.get("stdout") or ""),
        stderr=str(out.get("stderr") or ""),
        detail=out.get("detail"),
    )


@router.post("/sandbox/stop", status_code=status.HTTP_204_NO_CONTENT)
async def sandbox_stop(
    body: SandboxStopRequest,
    user: Annotated[User, Depends(get_current_user)],
) -> None:
    del user
    sandbox_service.stop_session(body.session_id)


@router.get("/results/{session_id}", response_model=TestResultsResponse)
async def testing_results(
    session_id: str,
    user: Annotated[User, Depends(get_current_user)],
) -> TestResultsResponse:
    del user
    blob = sandbox_service.get_last_result(session_id)
    if blob is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {"code": "RESULT_NOT_FOUND", "message": "No results yet", "details": {}},
            },
        )
    return TestResultsResponse(
        session_id=str(blob.get("session_id")),
        status=str(blob.get("status") or "unknown"),
        output=blob.get("output"),
    )
