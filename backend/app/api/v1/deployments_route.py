"""Deployments API (docs/API_SPEC.md §10)."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.deployment import Deployment
from app.models.user import User
from app.schemas.deployment import DeploymentCreate, DeploymentLogsResponse, DeploymentRead
from app.services import deployment_service

router = APIRouter(prefix="/deployments", tags=["deployments"])


@router.post("", response_model=DeploymentRead, status_code=status.HTTP_201_CREATED)
async def create_deployment(
    body: DeploymentCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Deployment:
    return await deployment_service.create_deployment(
        db,
        user,
        project_id=body.project_id,
        target=body.target,
    )


@router.get("/{deployment_id}", response_model=DeploymentRead)
async def get_deployment(
    deployment_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Deployment:
    row = await deployment_service.get_deployment(db, user, deployment_id)
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "DEPLOYMENT_NOT_FOUND",
                    "message": "Deployment not found",
                    "details": {},
                }
            },
        )
    return row


@router.get("/{deployment_id}/logs", response_model=DeploymentLogsResponse)
async def deployment_logs(
    deployment_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> DeploymentLogsResponse:
    row = await deployment_service.get_deployment(db, user, deployment_id)
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "DEPLOYMENT_NOT_FOUND",
                    "message": "Deployment not found",
                    "details": {},
                }
            },
        )
    msg = row.error_message or "No logs captured yet."
    return DeploymentLogsResponse(logs=[msg])


@router.delete("/{deployment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_deployment(
    deployment_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> None:
    row = await deployment_service.get_deployment(db, user, deployment_id)
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "DEPLOYMENT_NOT_FOUND",
                    "message": "Deployment not found",
                    "details": {},
                }
            },
        )
    await deployment_service.delete_deployment(db, row)
