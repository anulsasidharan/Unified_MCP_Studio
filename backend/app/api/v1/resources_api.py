import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.project import Project
from app.models.resource import Resource
from app.models.user import User
from app.schemas.resource import ResourceCreate, ResourcePublic, ResourceUpdate

router = APIRouter(tags=["resources"])


def _not_found() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error": {"code": "NOT_FOUND", "message": "Resource not found", "details": {}}},
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


async def _get_resource_owned(
    db: AsyncSession, resource_id: uuid.UUID, user_id: uuid.UUID
) -> Resource:
    result = await db.execute(select(Resource).where(Resource.id == resource_id))
    resource = result.scalar_one_or_none()
    if resource is None:
        raise _not_found()
    await _get_project(db, resource.project_id, user_id)
    return resource


@router.get("/projects/{project_id}/resources", response_model=list[ResourcePublic])
async def list_resources(
    project_id: uuid.UUID,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[Resource]:
    await _get_project(db, project_id, current.id)
    result = await db.execute(
        select(Resource).where(Resource.project_id == project_id).order_by(Resource.created_at)
    )
    return list(result.scalars().all())


@router.post(
    "/projects/{project_id}/resources",
    response_model=ResourcePublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_resource(
    project_id: uuid.UUID,
    body: ResourceCreate,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Resource:
    await _get_project(db, project_id, current.id)
    resource = Resource(
        project_id=project_id,
        name=body.name,
        uri=body.uri,
        description=body.description,
        mime_type=body.mime_type,
        provider_code=body.provider_code,
    )
    db.add(resource)
    await db.commit()
    await db.refresh(resource)
    return resource


@router.get("/resources/{resource_id}", response_model=ResourcePublic)
async def get_resource(
    resource_id: uuid.UUID,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Resource:
    return await _get_resource_owned(db, resource_id, current.id)


@router.put("/resources/{resource_id}", response_model=ResourcePublic)
async def update_resource(
    resource_id: uuid.UUID,
    body: ResourceUpdate,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Resource:
    resource = await _get_resource_owned(db, resource_id, current.id)
    if body.name is not None:
        resource.name = body.name
    if body.uri is not None:
        resource.uri = body.uri
    if body.description is not None:
        resource.description = body.description
    if body.mime_type is not None:
        resource.mime_type = body.mime_type
    if body.provider_code is not None:
        resource.provider_code = body.provider_code
    await db.commit()
    await db.refresh(resource)
    return resource


@router.delete("/resources/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(
    resource_id: uuid.UUID,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    resource = await _get_resource_owned(db, resource_id, current.id)
    await db.delete(resource)
    await db.commit()
