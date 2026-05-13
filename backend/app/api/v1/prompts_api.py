"""Prompts routes (docs/API_SPEC.md §6)."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.prompt import Prompt
from app.models.user import User
from app.schemas.prompt import PromptCreate, PromptRead, PromptUpdate
from app.services.access import require_project, require_prompt

proj_router = APIRouter(prefix="/projects/{project_id}/prompts", tags=["prompts"])
id_router = APIRouter(prefix="/prompts", tags=["prompts"])


@proj_router.get("", response_model=list[PromptRead])
async def list_prompts(
    project_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> list[Prompt]:
    await require_project(db, user, project_id)
    result = await db.execute(select(Prompt).where(Prompt.project_id == project_id))
    return list(result.scalars().all())


@proj_router.post("", response_model=PromptRead, status_code=status.HTTP_201_CREATED)
async def create_prompt(
    project_id: uuid.UUID,
    body: PromptCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Prompt:
    await require_project(db, user, project_id)
    row = Prompt(
        project_id=project_id,
        name=body.name,
        description=body.description,
        arguments=body.arguments,
        messages=body.messages,
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row


@id_router.get("/{prompt_id}", response_model=PromptRead)
async def get_prompt(
    prompt_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Prompt:
    return await require_prompt(db, user, prompt_id)


@id_router.put("/{prompt_id}", response_model=PromptRead)
async def update_prompt(
    prompt_id: uuid.UUID,
    body: PromptUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Prompt:
    row = await require_prompt(db, user, prompt_id)
    data = body.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(row, k, v)
    await db.commit()
    await db.refresh(row)
    return row


@id_router.delete("/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prompt(
    prompt_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> None:
    row = await require_prompt(db, user, prompt_id)
    await db.delete(row)
    await db.commit()
