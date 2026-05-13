"""Tool schemas (docs/API_SPEC.md §4)."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class ToolCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    input_schema: dict[str, Any]
    handler_code: str
    handler_language: str = Field(pattern="^(python|typescript)$")
    metadata: dict[str, Any] | None = Field(default=None)


class ToolUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    input_schema: dict[str, Any] | None = None
    handler_code: str | None = None
    handler_language: str | None = Field(default=None, pattern="^(python|typescript)$")
    metadata: dict[str, Any] | None = None


class ToolRead(BaseModel):
    id: UUID
    project_id: UUID
    name: str
    description: str | None
    input_schema: dict[str, Any]
    handler_code: str
    handler_language: str
    metadata: dict[str, Any] = Field(validation_alias="metadata_", serialization_alias="metadata")
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True, "populate_by_name": True}


class ToolTestRequest(BaseModel):
    arguments: dict[str, Any] = Field(default_factory=dict)


class ToolTestResponse(BaseModel):
    ok: bool
    stdout: str = ""
    stderr: str = ""
    result: Any | None = None
    detail: str | None = None
