"""Resources routes (docs/API_SPEC.md §5)."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.resource import Resource
from app.models.user import User
from app.schemas.resource import ResourceCreate, ResourceRead, ResourceUpdate
from app.services.access import require_project, require_resource

proj_router = APIRouter(prefix="/projects/{project_id}/resources", tags=["resources"])
id_router = APIRouter(prefix="/resources", tags=["resources"])


@proj_router.get("", response_model=list[ResourceRead])
async def list_resources(
    project_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> list[Resource]:
    await require_project(db, user, project_id)
    result = await db.execute(select(Resource).where(Resource.project_id == project_id))
    return list(result.scalars().all())


@proj_router.post("", response_model=ResourceRead, status_code=status.HTTP_201_CREATED)
async def create_resource(
    project_id: uuid.UUID,
    body: ResourceCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Resource:
    await require_project(db, user, project_id)
    row = Resource(
        project_id=project_id,
        uri=body.uri,
        name=body.name,
        description=body.description,
        mime_type=body.mime_type,
        provider_code=body.provider_code,
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row


@id_router.get("/{resource_id}", response_model=ResourceRead)
async def get_resource(
    resource_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Resource:
    return await require_resource(db, user, resource_id)


@id_router.put("/{resource_id}", response_model=ResourceRead)
async def update_resource(
    resource_id: uuid.UUID,
    body: ResourceUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Resource:
    row = await require_resource(db, user, resource_id)
    data = body.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(row, k, v)
    await db.commit()
    await db.refresh(row)
    return row


@id_router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(
    resource_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> None:
    row = await require_resource(db, user, resource_id)
    await db.delete(row)
    await db.commit()
