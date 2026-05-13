import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.project import Project
from app.models.prompt import Prompt
from app.models.user import User
from app.schemas.prompt import PromptCreate, PromptPublic, PromptUpdate

router = APIRouter(tags=["prompts"])


def _not_found() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error": {"code": "NOT_FOUND", "message": "Prompt not found", "details": {}}},
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


async def _get_prompt_owned(
    db: AsyncSession, prompt_id: uuid.UUID, user_id: uuid.UUID
) -> Prompt:
    result = await db.execute(select(Prompt).where(Prompt.id == prompt_id))
    prompt = result.scalar_one_or_none()
    if prompt is None:
        raise _not_found()
    await _get_project(db, prompt.project_id, user_id)
    return prompt


@router.get("/projects/{project_id}/prompts", response_model=list[PromptPublic])
async def list_prompts(
    project_id: uuid.UUID,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[Prompt]:
    await _get_project(db, project_id, current.id)
    result = await db.execute(
        select(Prompt).where(Prompt.project_id == project_id).order_by(Prompt.created_at)
    )
    return list(result.scalars().all())


@router.post(
    "/projects/{project_id}/prompts",
    response_model=PromptPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_prompt(
    project_id: uuid.UUID,
    body: PromptCreate,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Prompt:
    await _get_project(db, project_id, current.id)
    prompt = Prompt(
        project_id=project_id,
        name=body.name,
        description=body.description,
        arguments=body.arguments,
        messages=body.messages,
    )
    db.add(prompt)
    await db.commit()
    await db.refresh(prompt)
    return prompt


@router.get("/prompts/{prompt_id}", response_model=PromptPublic)
async def get_prompt(
    prompt_id: uuid.UUID,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Prompt:
    return await _get_prompt_owned(db, prompt_id, current.id)


@router.put("/prompts/{prompt_id}", response_model=PromptPublic)
async def update_prompt(
    prompt_id: uuid.UUID,
    body: PromptUpdate,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Prompt:
    prompt = await _get_prompt_owned(db, prompt_id, current.id)
    if body.name is not None:
        prompt.name = body.name
    if body.description is not None:
        prompt.description = body.description
    if body.arguments is not None:
        prompt.arguments = body.arguments
    if body.messages is not None:
        prompt.messages = body.messages
    await db.commit()
    await db.refresh(prompt)
    return prompt


@router.delete("/prompts/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prompt(
    prompt_id: uuid.UUID,
    current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    prompt = await _get_prompt_owned(db, prompt_id, current.id)
    await db.delete(prompt)
    await db.commit()
