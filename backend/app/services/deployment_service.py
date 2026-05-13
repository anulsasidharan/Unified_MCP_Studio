"""Deployments CRUD + worker hand-off (Phase 7)."""

from __future__ import annotations

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.deployment import Deployment
from app.models.project import Project
from app.models.user import User
from app.services.access import require_project


async def create_deployment(
    db: AsyncSession,
    user: User,
    *,
    project_id: uuid.UUID,
    target: str,
) -> Deployment:
    await require_project(db, user, project_id)
    row = Deployment(project_id=project_id, target=target, status="pending")
    db.add(row)
    await db.commit()
    await db.refresh(row)

    if target == "cloud_run":
        from app.workers.tasks import deploy_cloud_run

        deploy_cloud_run.delay(str(row.id))
    elif target == "local":
        row.status = "deployed"
        row.url = "http://localhost"
        await db.commit()
        await db.refresh(row)

    return row


async def get_deployment(
    db: AsyncSession,
    user: User,
    deployment_id: uuid.UUID,
) -> Deployment | None:
    result = await db.execute(
        select(Deployment)
        .join(Project, Deployment.project_id == Project.id)
        .where(Deployment.id == deployment_id, Project.user_id == user.id),
    )
    return result.scalar_one_or_none()


async def delete_deployment(db: AsyncSession, deployment: Deployment) -> None:
    await db.delete(deployment)
    await db.commit()


async def count_deployments(db: AsyncSession, user: User) -> int:
    q = await db.scalar(
        select(func.count())
        .select_from(Deployment)
        .join(Project, Deployment.project_id == Project.id)
        .where(Project.user_id == user.id),
    )
    return int(q or 0)
