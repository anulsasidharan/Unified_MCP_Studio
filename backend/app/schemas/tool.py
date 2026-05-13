from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

_DEFAULT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {},
    "additionalProperties": False,
}


class ToolCreate(BaseModel):
    name: str = Field(max_length=255)
    description: str | None = None
    input_schema: dict[str, Any] = Field(default_factory=lambda: dict(_DEFAULT_SCHEMA))
    handler_code: str = Field(default="")
    handler_language: str = Field(default="python", max_length=50)


class ToolUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = None
    input_schema: dict[str, Any] | None = None
    handler_code: str | None = None
    handler_language: str | None = Field(default=None, max_length=50)


class ToolPublic(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    project_id: UUID
    name: str
    description: str | None
    input_schema: dict[str, Any]
    handler_code: str
    handler_language: str
    created_at: datetime
    updated_at: datetime
