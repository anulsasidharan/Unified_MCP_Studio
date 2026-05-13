"""Resource schemas (docs/API_SPEC.md §5)."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ResourceCreate(BaseModel):
    uri: str = Field(min_length=1, max_length=500)
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    mime_type: str | None = Field(default=None, max_length=100)
    provider_code: str


class ResourceUpdate(BaseModel):
    uri: str | None = Field(default=None, min_length=1, max_length=500)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    mime_type: str | None = Field(default=None, max_length=100)
    provider_code: str | None = None


class ResourceRead(BaseModel):
    id: UUID
    project_id: UUID
    uri: str
    name: str
    description: str | None
    mime_type: str | None
    provider_code: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
