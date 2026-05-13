"""Library template schemas (Phase 6)."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class FromTemplateCreate(BaseModel):
    template_id: UUID


class TemplateRead(BaseModel):
    id: UUID
    name: str
    description: str | None
    category: str | None
    is_public: bool
    author_id: UUID | None
    use_count: int
    config: dict[str, Any]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
