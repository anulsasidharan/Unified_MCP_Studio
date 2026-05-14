"""Code generation and download endpoints."""

import re
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services.codegen_service import generate_project_files, make_zip

router = APIRouter(tags=["codegen"])


class GeneratedFile(BaseModel):
    path: str
    content: str


class GenerateResponse(BaseModel):
    runtime: str
    project_name: str
    files: list[GeneratedFile]


def _not_found() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error": {"code": "NOT_FOUND", "message": "Project not found", "details": {}}},
    )


@router.post("/projects/{project_id}/generate", response_model=GenerateResponse)
async def generate_code(
    project_id: UUID,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> GenerateResponse:
    files, project = await generate_project_files(db, project_id, current.id)
    if files is None:
        raise _not_found()
    return GenerateResponse(
        runtime=project.runtime,
        project_name=project.name,
        files=[GeneratedFile(path=p, content=c) for p, c in sorted(files.items())],
    )


@router.get("/projects/{project_id}/download")
async def download_code(
    project_id: UUID,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Response:
    files, project = await generate_project_files(db, project_id, current.id)
    if files is None:
        raise _not_found()

    zip_bytes = make_zip(files)
    safe_name = re.sub(r"[^a-z0-9\-]", "-", project.name.lower().replace(" ", "-")).strip("-")

    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{safe_name}-mcp-server.zip"'},
    )
