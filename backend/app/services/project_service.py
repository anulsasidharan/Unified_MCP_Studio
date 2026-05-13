"""Project persistence."""

from __future__ import annotations

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate


async def count_projects(db: AsyncSession, user: User) -> int:
    q = await db.scalar(select(func.count()).select_from(Project).where(Project.user_id == user.id))
    return int(q or 0)


async def list_projects(
    db: AsyncSession,
    user: User,
    *,
    skip: int,
    limit: int,
) -> list[Project]:
    result = await db.execute(
        select(Project)
        .where(Project.user_id == user.id)
        .order_by(Project.updated_at.desc())
        .offset(skip)
        .limit(limit),
    )
    return list(result.scalars().all())


async def create_project(db: AsyncSession, user: User, body: ProjectCreate) -> Project:
    p = Project(
        user_id=user.id,
        name=body.name,
        description=body.description,
        runtime=body.runtime,
        transport=body.transport,
        config=body.config or {},
    )
    db.add(p)
    await db.commit()
    await db.refresh(p)
    return p


async def update_project(db: AsyncSession, project: Project, body: ProjectUpdate) -> Project:
    data = body.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(project, k, v)
    await db.commit()
    await db.refresh(project)
    return project


async def delete_project(db: AsyncSession, project: Project) -> None:
    await db.delete(project)
    await db.commit()


async def get_project_with_children(
    db: AsyncSession,
    project_id: uuid.UUID,
) -> Project | None:
    from sqlalchemy.orm import selectinload

    result = await db.execute(
        select(Project)
        .where(Project.id == project_id)
        .options(
            selectinload(Project.tools),
            selectinload(Project.resources),
            selectinload(Project.prompts),
        ),
    )
    return result.scalar_one_or_none()
