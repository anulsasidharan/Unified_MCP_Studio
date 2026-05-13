"""Sandbox session registry + subprocess execution (Phase 5)."""

from __future__ import annotations

import json
import logging
import os
import re
import subprocess
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.tool import Tool
from app.services import codegen_service
from app.services.validation_service import validate_payload_against_tool_schema

logger = logging.getLogger(__name__)

try:
    import redis

    _redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
    try:
        _redis_client.ping()
    except Exception:
        _redis_client = None  # type: ignore[assignment]
except Exception:
    _redis_client = None

_memory_sessions: dict[str, dict[str, Any]] = {}
_memory_results: dict[str, dict[str, Any]] = {}


def _store(session_id: str, payload: dict[str, Any]) -> None:
    ttl = 3600
    raw = json.dumps(payload)
    if _redis_client is not None:
        _redis_client.setex(f"sandbox:session:{session_id}", ttl, raw)
    else:
        _memory_sessions[session_id] = payload


def get_session_payload(session_id: str) -> dict[str, Any] | None:
    """Return sandbox session metadata if present."""
    return _load(session_id)


def _load(session_id: str) -> dict[str, Any] | None:
    if _redis_client is not None:
        raw = _redis_client.get(f"sandbox:session:{session_id}")
        if not raw:
            return None
        return json.loads(raw)
    return _memory_sessions.get(session_id)


def _delete(session_id: str) -> None:
    if _redis_client is not None:
        _redis_client.delete(f"sandbox:session:{session_id}")
    else:
        _memory_sessions.pop(session_id, None)


def _slug(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_]+", "_", text.strip()).strip("_")
    if not s:
        s = "tool"
    if s[0].isdigit():
        s = f"t_{s}"
    return s.lower()


@dataclass
class SandboxSession:
    session_id: str
    project_id: uuid.UUID
    bundle_dir: str
    runtime: str


async def start_session(db: AsyncSession, project_id: uuid.UUID) -> SandboxSession:
    project, bundle_dir = await codegen_service.materialize_project_tree(db, project_id)
    sid = uuid.uuid4().hex
    _store(
        sid,
        {
            "project_id": str(project.id),
            "bundle_dir": str(bundle_dir),
            "runtime": project.runtime,
        },
    )
    return SandboxSession(
        session_id=sid,
        project_id=project.id,
        bundle_dir=str(bundle_dir),
        runtime=project.runtime,
    )


async def execute_tool(
    db: AsyncSession,
    *,
    session_id: str,
    tool: Tool,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    del db  # reserved for future auditing
    payload = _load(session_id)
    if payload is None:
        return {"ok": False, "stderr": "", "stdout": "", "detail": "unknown session"}
    if str(tool.project_id) != payload["project_id"]:
        return {"ok": False, "stderr": "", "stdout": "", "detail": "tool/project mismatch"}
    try:
        validate_payload_against_tool_schema(tool.input_schema, arguments)
    except Exception as exc:
        return {
            "ok": False,
            "stderr": repr(exc),
            "stdout": "",
            "detail": "schema validation failed",
        }

    runtime = payload["runtime"]
    bundle_path = Path(payload["bundle_dir"])
    if runtime != "python":
        return {
            "ok": False,
            "stderr": "",
            "stdout": "",
            "detail": "sandbox execute supports python runtime only in this MVP",
        }

    mod = f"generated_mcp.tools.{_slug(tool.name)}"
    argv = [
        sys.executable,
        str(bundle_path / "studio_execute.py"),
        mod,
        json.dumps(arguments, ensure_ascii=False),
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(bundle_path / "src")
    try:
        proc = subprocess.run(
            argv,
            cwd=str(bundle_path),
            env=env,
            capture_output=True,
            text=True,
            timeout=settings.sandbox_subprocess_timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "stderr": "timeout", "stdout": "", "detail": "timeout"}

    out = (proc.stdout or "")[-settings.sandbox_max_output_bytes :]
    err = (proc.stderr or "")[-settings.sandbox_max_output_bytes :]
    ok = proc.returncode == 0
    logger.info(
        "sandbox_execute",
        extra={"session_id": session_id, "tool": tool.name, "rc": proc.returncode},
    )
    result = {"ok": ok, "stdout": out, "stderr": err, "detail": None if ok else "non-zero exit"}
    _store_result(session_id, result)
    return result


def stop_session(session_id: str) -> None:
    _delete(session_id)


def _store_result(session_id: str, payload: dict[str, Any]) -> None:
    blob = {"session_id": session_id, "status": "ok", "output": payload}
    raw = json.dumps(blob)
    if _redis_client is not None:
        _redis_client.setex(f"sandbox:result:{session_id}", 3600, raw)
    else:
        _memory_results[session_id] = blob


def get_last_result(session_id: str) -> dict[str, Any] | None:
    if _redis_client is not None:
        raw = _redis_client.get(f"sandbox:result:{session_id}")
        if not raw:
            return None
        return json.loads(raw)
    return _memory_results.get(session_id)
