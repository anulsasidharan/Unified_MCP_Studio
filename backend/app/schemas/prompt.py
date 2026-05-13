"""Prompt schemas (docs/API_SPEC.md §6)."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class PromptCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    arguments: list[Any] = Field(default_factory=list)
    messages: list[Any] = Field(default_factory=list)


class PromptUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    arguments: list[Any] | None = None
    messages: list[Any] | None = None


class PromptRead(BaseModel):
    id: UUID
    project_id: UUID
    name: str
    description: str | None
    arguments: list[Any]
    messages: list[Any]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
