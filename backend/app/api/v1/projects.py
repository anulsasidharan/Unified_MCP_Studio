"""Projects CRUD + validate/generate/download (docs/API_SPEC.md §3, §7)."""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.project import Project
from app.models.user import User
from app.schemas.codegen import GenerateResponse
from app.schemas.project import (
    ProjectCreate,
    ProjectListResponse,
    ProjectRead,
    ProjectUpdate,
    ValidateResult,
)
from app.schemas.template_lib import FromTemplateCreate
from app.services import codegen_service, project_service, template_service
from app.services.access import require_project
from app.services.validation_service import validate_project_bundle

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=ProjectListResponse)
async def list_projects(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> ProjectListResponse:
    skip = (page - 1) * page_size
    total = await project_service.count_projects(db, user)
    rows = await project_service.list_projects(db, user, skip=skip, limit=page_size)
    return ProjectListResponse(
        items=[ProjectRead.model_validate(r) for r in rows],
        page=page,
        page_size=page_size,
        total=total,
    )


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    body: ProjectCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Project:
    p = await project_service.create_project(db, user, body)
    return p


@router.post("/from-template", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_from_template(
    body: FromTemplateCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Project:
    try:
        return await template_service.instantiate_template(db, user, body.template_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "TEMPLATE_NOT_FOUND",
                    "message": str(exc),
                    "details": {},
                }
            },
        ) from exc


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Project:
    return await require_project(db, user, project_id)


@router.put("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: uuid.UUID,
    body: ProjectUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Project:
    p = await require_project(db, user, project_id)
    return await project_service.update_project(db, p, body)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> None:
    p = await require_project(db, user, project_id)
    await project_service.delete_project(db, p)


@router.post("/{project_id}/validate", response_model=ValidateResult)
async def validate_project(
    project_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> ValidateResult:
    await require_project(db, user, project_id)
    full = await project_service.get_project_with_children(db, project_id)
    if full is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {"code": "NOT_FOUND", "message": "Project not found", "details": {}},
            },
        )
    issues = validate_project_bundle(
        project=full,
        tools=list(full.tools),
        resources=list(full.resources),
        prompts=list(full.prompts),
    )
    return ValidateResult(valid=len(issues) == 0, issues=issues)


@router.post("/{project_id}/generate", response_model=GenerateResponse)
async def generate_project(
    project_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> GenerateResponse:
    await require_project(db, user, project_id)
    if settings.codegen_use_celery:
        from app.workers.tasks import codegen_bundle

        task = codegen_bundle.delay(str(project_id))
        return GenerateResponse(task_id=task.id, status="queued", artifact=None)

    meta = await codegen_service.write_zip_artifact(db, project_id)
    return GenerateResponse(task_id=None, status="completed", artifact=meta)


@router.get("/{project_id}/download")
async def download_project(
    project_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    p = await require_project(db, user, project_id)
    cfg = dict(p.config or {})
    art = cfg.get("artifact") or {}
    path = art.get("path")
    if not path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "ARTIFACT_MISSING",
                    "message": "Generate the project before downloading",
                    "details": {},
                }
            },
        )
    fp = Path(path)
    if not fp.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "ARTIFACT_NOT_ON_DISK",
                    "message": "Artifact file not found",
                    "details": {},
                }
            },
        )

    if settings.gcs_bucket:
        try:
            from google.cloud import storage  # type: ignore

            client = storage.Client()
            blob_name = f"artifacts/{project_id}/{fp.name}"
            bucket = client.bucket(settings.gcs_bucket)
            blob = bucket.blob(blob_name)
            blob.upload_from_filename(str(fp))
            url = blob.generate_signed_url(
                version="v4",
                expiration=settings.gcs_sign_ttl_seconds,
                method="GET",
            )
            return RedirectResponse(url)
        except Exception:
            pass

    filename = str(art.get("filename") or "bundle.zip")
    return FileResponse(path=str(fp), filename=filename, media_type="application/zip")
