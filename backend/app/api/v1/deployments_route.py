"""Deployment management endpoints."""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.deployment import Deployment
from app.models.project import Project
from app.models.user import User

router = APIRouter(prefix="/deployments", tags=["deployments"])


class DeploymentCreate(BaseModel):
    project_id: UUID
    target: str


class DeploymentPublic(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    project_id: UUID
    target: str
    status: str
    url: str | None
    error_message: str | None


async def _get_owned_deployment(
    db: AsyncSession, deployment_id: UUID, user_id: UUID
) -> Deployment:
    result = await db.execute(
        select(Deployment).join(Project).where(
            Deployment.id == deployment_id,
            Project.user_id == user_id,
        )
    )
    d = result.scalar_one_or_none()
    if d is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "NOT_FOUND", "message": "Deployment not found", "details": {}}},
        )
    return d


@router.post("", response_model=DeploymentPublic, status_code=status.HTTP_201_CREATED)
async def create_deployment(
    body: DeploymentCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Deployment:
    proj_result = await db.execute(
        select(Project).where(
            Project.id == body.project_id,
            Project.user_id == current_user.id,
        )
    )
    project = proj_result.scalar_one_or_none()
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "NOT_FOUND", "message": "Project not found", "details": {}}},
        )
    d = Deployment(
        project_id=body.project_id,
        target=body.target,
        status="pending",
    )
    db.add(d)
    await db.commit()
    await db.refresh(d)
    return d


@router.get("/{deployment_id}", response_model=DeploymentPublic)
async def get_deployment(
    deployment_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Deployment:
    return await _get_owned_deployment(db, deployment_id, current_user.id)


@router.get("/{deployment_id}/logs")
async def get_deployment_logs(
    deployment_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, Any]:
    await _get_owned_deployment(db, deployment_id, current_user.id)
    return {"logs": []}


@router.delete("/{deployment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_deployment(
    deployment_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    d = await _get_owned_deployment(db, deployment_id, current_user.id)
    await db.delete(d)
    await db.commit()
