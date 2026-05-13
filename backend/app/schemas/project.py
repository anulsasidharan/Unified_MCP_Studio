from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(max_length=255)
    description: str | None = None
    runtime: str = Field(default="python", max_length=50)
    transport: str = Field(default="stdio", max_length=50)
    config: dict[str, Any] = Field(default_factory=dict)


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = None
    config: dict[str, Any] | None = None


class ProjectPublic(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    user_id: UUID
    name: str
    description: str | None
    runtime: str
    transport: str
    config: dict[str, Any]
    created_at: datetime
    updated_at: datetime
