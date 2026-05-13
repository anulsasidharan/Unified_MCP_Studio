"""Codegen job payloads."""

from typing import Any

from pydantic import BaseModel


class GenerateQueued(BaseModel):
    task_id: str
    status: str = "queued"


class GenerateCompleted(BaseModel):
    status: str = "completed"
    artifact: dict[str, Any]


class GenerateResponse(BaseModel):
    """Either queued Celery task or inline artifact metadata."""

    task_id: str | None = None
    status: str
    artifact: dict[str, Any] | None = None
