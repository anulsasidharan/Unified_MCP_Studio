"""JSON Schema validation for stored definitions (TASKS Phase 3 — SI 13)."""

from __future__ import annotations

from typing import Any

import jsonschema
from jsonschema import Draft202012Validator

from app.models.project import Project
from app.models.prompt import Prompt
from app.models.resource import Resource
from app.models.tool import Tool


def _validate_json_schema(instance: dict[str, Any]) -> None:
    Draft202012Validator.check_schema(instance)


def validate_tool_input_schema(schema: dict[str, Any]) -> None:
    _validate_json_schema(schema)


def validate_project_bundle(
    *,
    project: Project,
    tools: list[Tool],
    resources: list[Resource],
    prompts: list[Prompt],
) -> list[str]:
    """Return a list of human-readable issues; empty means valid."""
    issues: list[str] = []

    if project.runtime not in ("typescript", "python"):
        issues.append(f"Unsupported runtime: {project.runtime}")
    if project.transport not in ("stdio", "sse"):
        issues.append(f"Unsupported transport: {project.transport}")

    names_seen: set[str] = set()
    for t in tools:
        if t.name in names_seen:
            issues.append(f"Duplicate tool name: {t.name}")
        names_seen.add(t.name)
        try:
            validate_tool_input_schema(t.input_schema)
        except jsonschema.SchemaError as exc:
            issues.append(f"Tool {t.name} input_schema invalid: {exc.message}")

    uri_seen: set[str] = set()
    for r in resources:
        if r.uri in uri_seen:
            issues.append(f"Duplicate resource URI: {r.uri}")
        uri_seen.add(r.uri)

    pname: set[str] = set()
    for p in prompts:
        if p.name in pname:
            issues.append(f"Duplicate prompt name: {p.name}")
        pname.add(p.name)
        if not isinstance(p.arguments, list):
            issues.append(f"Prompt {p.name}: arguments must be a JSON array")
        if not isinstance(p.messages, list):
            issues.append(f"Prompt {p.name}: messages must be a JSON array")

    return issues


def validate_payload_against_tool_schema(schema: dict[str, Any], payload: dict[str, Any]) -> None:
    validate_tool_input_schema(schema)
    jsonschema.validate(instance=payload, schema=schema)
