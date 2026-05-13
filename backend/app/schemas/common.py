"""Shared API types."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    error: dict[str, Any]


class PaginatedParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class UserSummary(BaseModel):
    id: UUID
    email: str
    name: str | None
    tier: str
    created_at: datetime

    model_config = {"from_attributes": True}
