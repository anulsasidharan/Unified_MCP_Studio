"""Testing / sandbox API (docs/API_SPEC.md §9)."""

from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class SandboxStartRequest(BaseModel):
    project_id: UUID


class SandboxStartResponse(BaseModel):
    session_id: str


class SandboxExecuteRequest(BaseModel):
    session_id: str
    tool_name: str = Field(min_length=1)
    arguments: dict[str, Any] = Field(default_factory=dict)


class SandboxExecuteResponse(BaseModel):
    ok: bool
    stdout: str = ""
    stderr: str = ""
    detail: str | None = None


class SandboxStopRequest(BaseModel):
    session_id: str


class TestResultsResponse(BaseModel):
    session_id: str
    status: str
    output: dict[str, Any] | None = None
