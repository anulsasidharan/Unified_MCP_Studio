from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class ProjectFromTemplateCreate(BaseModel):
    template_id: UUID
    name: str | None = Field(default=None, max_length=255)


class ProjectFromCatalogBlueprintCreate(BaseModel):
    blueprint_id: str = Field(..., min_length=1, max_length=220)
    name: str | None = Field(default=None, max_length=255)


class CatalogBlueprintImport(BaseModel):
    """Validated JSON export from the template catalog (single blueprint)."""

    id: str = Field(..., min_length=1, max_length=220)
    tier: str = Field(..., min_length=1, max_length=32)
    name: str = Field(..., min_length=1, max_length=255)
    project_name: str | None = Field(default=None, max_length=255)
    tagline: str = Field(default="", max_length=4000)
    category: str = Field(default="", max_length=120)
    primaryRuntime: Literal["typescript", "python"]
    transport: Literal["stdio", "sse"]
    overview: str = Field(default="", max_length=16000)
    design: str = Field(default="", max_length=32000)
    extensionIdeas: str = Field(default="", max_length=8000)
    risks: str = Field(default="", max_length=8000)
    suggestedTools: list[str] = Field(min_length=1, max_length=48)

    @field_validator("suggestedTools")
    @classmethod
    def strip_tool_names(cls, v: list[str]) -> list[str]:
        out: list[str] = []
        for i, raw in enumerate(v):
            if not isinstance(raw, str) or not raw.strip():
                raise ValueError(f"suggestedTools[{i}] must be a non-empty string")
            out.append(raw.strip())
        return out


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
