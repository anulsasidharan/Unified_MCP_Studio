"""Library template catalog (docs/API_SPEC.md §8)."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.library_template import LibraryTemplate
from app.schemas.template_lib import TemplateRead
from app.services import template_service

router = APIRouter(prefix="/templates", tags=["templates"])


@router.get("", response_model=list[TemplateRead])
async def list_templates(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> list[LibraryTemplate]:
    skip = (page - 1) * page_size
    rows, _total = await template_service.list_templates(db, skip=skip, limit=page_size)
    return rows


@router.get("/{template_id}", response_model=TemplateRead)
async def get_template(
    template_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LibraryTemplate:
    tpl = await template_service.get_template(db, template_id)
    if tpl is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "TEMPLATE_NOT_FOUND",
                    "message": "Template not found",
                    "details": {},
                }
            },
        )
    return tpl
