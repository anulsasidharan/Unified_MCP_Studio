"""Project request/response (docs/API_SPEC.md §3)."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    runtime: str = Field(pattern="^(typescript|python)$")
    transport: str = Field(pattern="^(stdio|sse)$")
    config: dict[str, Any] = Field(default_factory=dict)


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    runtime: str | None = Field(default=None, pattern="^(typescript|python)$")
    transport: str | None = Field(default=None, pattern="^(stdio|sse)$")
    config: dict[str, Any] | None = None


class ProjectRead(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    description: str | None
    runtime: str
    transport: str
    config: dict[str, Any]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProjectListResponse(BaseModel):
    items: list[ProjectRead]
    page: int
    page_size: int
    total: int


class ValidateResult(BaseModel):
    valid: bool
    issues: list[str]
