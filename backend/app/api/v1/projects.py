import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.project import Project
from app.models.user import User
from app.schemas.project import (
    CatalogBlueprintImport,
    ProjectCreate,
    ProjectFromCatalogBlueprintCreate,
    ProjectFromTemplateCreate,
    ProjectPublic,
    ProjectUpdate,
)
from app.services.catalog_blueprint_service import (
    create_project_from_blueprint_dict,
    create_project_from_catalog_blueprint_id,
)
from app.services.template_project_service import create_project_from_library_template

router = APIRouter(prefix="/projects", tags=["projects"])


def _not_found() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error": {"code": "NOT_FOUND", "message": "Project not found", "details": {}}},
    )


async def _get_owned(db: AsyncSession, project_id: uuid.UUID, user_id: uuid.UUID) -> Project:
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if project is None or project.user_id != user_id:
        raise _not_found()
    return project


@router.get("", response_model=list[ProjectPublic])
async def list_projects(
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[Project]:
    result = await db.execute(
        select(Project).where(Project.user_id == current.id).order_by(Project.created_at.desc())
    )
    return list(result.scalars().all())


@router.post("", response_model=ProjectPublic, status_code=status.HTTP_201_CREATED)
async def create_project(
    body: ProjectCreate,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Project:
    project = Project(
        user_id=current.id,
        name=body.name,
        description=body.description,
        runtime=body.runtime,
        transport=body.transport,
        config=body.config,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


@router.post(
    "/from-template",
    response_model=ProjectPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_project_from_template(
    body: ProjectFromTemplateCreate,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Project:
    return await create_project_from_library_template(
        db,
        user_id=current.id,
        template_id=body.template_id,
        project_name=body.name,
    )


@router.post(
    "/from-catalog-blueprint",
    response_model=ProjectPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_project_from_catalog_blueprint(
    body: ProjectFromCatalogBlueprintCreate,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Project:
    return await create_project_from_catalog_blueprint_id(
        db,
        user_id=current.id,
        blueprint_id=body.blueprint_id,
        project_name=body.name,
    )


@router.post(
    "/from-blueprint-export",
    response_model=ProjectPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_project_from_blueprint_export(
    body: CatalogBlueprintImport,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Project:
    raw = body.model_dump()
    project_name = raw.pop("project_name", None)
    return await create_project_from_blueprint_dict(
        db,
        user_id=current.id,
        blueprint=raw,
        project_name=project_name,
    )


@router.get("/{project_id}", response_model=ProjectPublic)
async def get_project(
    project_id: uuid.UUID,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Project:
    return await _get_owned(db, project_id, current.id)


@router.put("/{project_id}", response_model=ProjectPublic)
async def update_project(
    project_id: uuid.UUID,
    body: ProjectUpdate,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Project:
    project = await _get_owned(db, project_id, current.id)
    if body.name is not None:
        project.name = body.name
    if body.description is not None:
        project.description = body.description
    if body.config is not None:
        project.config = body.config
    await db.commit()
    await db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: uuid.UUID,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    project = await _get_owned(db, project_id, current.id)
    await db.delete(project)
    await db.commit()
