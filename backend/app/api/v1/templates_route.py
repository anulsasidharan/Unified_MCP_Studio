from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.library_template import LibraryTemplate
from app.models.user import User

from datetime import datetime
from typing import Any
from uuid import UUID
from pydantic import BaseModel

router = APIRouter(prefix="/templates", tags=["templates"])


class TemplatePublic(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    name: str
    description: str | None
    category: str | None
    is_public: bool
    use_count: int
    config: dict[str, Any]
    created_at: datetime
    updated_at: datetime


@router.get("", response_model=list[TemplatePublic])
async def list_templates(
    _current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[LibraryTemplate]:
    result = await db.execute(
        select(LibraryTemplate)
        .where(LibraryTemplate.is_public == True)  # noqa: E712
        .order_by(LibraryTemplate.use_count.desc(), LibraryTemplate.created_at)
    )
    return list(result.scalars().all())


@router.get("/{template_id}", response_model=TemplatePublic)
async def get_template(
    template_id: UUID,
    _current: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LibraryTemplate:
    from fastapi import HTTPException, status
    result = await db.execute(
        select(LibraryTemplate).where(LibraryTemplate.id == template_id)
    )
    t = result.scalar_one_or_none()
    if t is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"error": {"code": "NOT_FOUND", "message": "Template not found", "details": {}}})
    return t
