"""Deployment schemas (docs/API_SPEC.md §10)."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class DeploymentCreate(BaseModel):
    project_id: UUID
    target: str = Field(pattern="^(local|cloud_run|lambda|docker)$")


class DeploymentRead(BaseModel):
    id: UUID
    project_id: UUID
    target: str
    status: str
    url: str | None
    error_message: str | None
    deployed_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class DeploymentLogsResponse(BaseModel):
    logs: list[str]
