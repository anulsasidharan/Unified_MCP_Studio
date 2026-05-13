from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ResourceCreate(BaseModel):
    name: str = Field(max_length=255)
    uri: str = Field(default="resource://", max_length=500)
    description: str | None = None
    mime_type: str | None = Field(default="text/plain", max_length=100)
    provider_code: str = Field(default="")


class ResourceUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    uri: str | None = Field(default=None, max_length=500)
    description: str | None = None
    mime_type: str | None = Field(default=None, max_length=100)
    provider_code: str | None = None


class ResourcePublic(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    project_id: UUID
    name: str
    uri: str
    description: str | None
    mime_type: str | None
    provider_code: str
    created_at: datetime
    updated_at: datetime
