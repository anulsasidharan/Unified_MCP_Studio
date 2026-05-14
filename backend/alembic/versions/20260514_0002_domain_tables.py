"""Domain tables: projects, tools, resources, prompts, test_cases, library_templates, deployments.

Revision ID: 20260514_0002
Revises: 20260513_0001
Create Date: 2026-05-14

"""

from typing import Sequence, Union
import uuid

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260514_0002"
down_revision: Union[str, Sequence[str], None] = "20260513_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── projects ──────────────────────────────────────────────────────────────
    op.create_table(
        "projects",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("runtime", sa.String(50), nullable=False),
        sa.Column("transport", sa.String(50), nullable=False),
        sa.Column(
            "config",
            postgresql.JSONB(),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_projects_user_id", "projects", ["user_id"])

    # ── tools ─────────────────────────────────────────────────────────────────
    op.create_table(
        "tools",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("input_schema", postgresql.JSONB(), nullable=False),
        sa.Column("handler_code", sa.Text(), nullable=False),
        sa.Column("handler_language", sa.String(50), nullable=False),
        sa.Column(
            "metadata",
            postgresql.JSONB(),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_tools_project_id", "tools", ["project_id"])

    # ── resources ─────────────────────────────────────────────────────────────
    op.create_table(
        "resources",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("uri", sa.String(500), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("mime_type", sa.String(100), nullable=True),
        sa.Column("provider_code", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_resources_project_id", "resources", ["project_id"])

    # ── prompts ───────────────────────────────────────────────────────────────
    op.create_table(
        "prompts",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "arguments",
            postgresql.JSONB(),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "messages",
            postgresql.JSONB(),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_prompts_project_id", "prompts", ["project_id"])

    # ── library_templates ─────────────────────────────────────────────────────
    op.create_table(
        "library_templates",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(100), nullable=True),
        sa.Column("is_public", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("author_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("use_count", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("config", postgresql.JSONB(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_library_templates_category", "library_templates", ["category"])

    # ── test_cases ────────────────────────────────────────────────────────────
    op.create_table(
        "test_cases",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("tool_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("input_data", postgresql.JSONB(), nullable=False),
        sa.Column("expected_output", postgresql.JSONB(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["tool_id"], ["tools.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_test_cases_tool_id", "test_cases", ["tool_id"])

    # ── deployments ───────────────────────────────────────────────────────────
    op.create_table(
        "deployments",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("target", sa.String(100), nullable=False),
        sa.Column("status", sa.String(50), nullable=False),
        sa.Column("url", sa.String(500), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("deployed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_deployments_project_id", "deployments", ["project_id"])

    # ── seed starter templates ────────────────────────────────────────────────
    library_templates = sa.table(
        "library_templates",
        sa.column("id", postgresql.UUID(as_uuid=True)),
        sa.column("name", sa.String),
        sa.column("description", sa.Text),
        sa.column("category", sa.String),
        sa.column("is_public", sa.Boolean),
        sa.column("author_id", postgresql.UUID(as_uuid=True)),
        sa.column("use_count", sa.Integer),
        sa.column("config", postgresql.JSONB),
    )
    op.bulk_insert(
        library_templates,
        [
            {
                "id": uuid.UUID("00000000-0000-0000-0000-000000000001"),
                "name": "REST API Wrapper",
                "description": "Generic HTTP client that wraps any REST API. Includes a fetch_json tool with configurable base URL, path, method, and headers.",
                "category": "api",
                "is_public": True,
                "author_id": None,
                "use_count": 0,
                "config": {
                    "runtime": "python",
                    "transport": "stdio",
                    "tools": [
                        {
                            "name": "fetch_json",
                            "description": "Fetch JSON from a REST API endpoint",
                            "input_schema": {
                                "type": "object",
                                "properties": {
                                    "url": {"type": "string", "description": "Full URL to fetch"},
                                    "method": {"type": "string", "enum": ["GET", "POST", "PUT", "DELETE"], "default": "GET"},
                                    "body": {"type": "object", "description": "Request body (POST/PUT only)"},
                                },
                                "required": ["url"],
                            },
                            "handler_code": "import httpx\nasync with httpx.AsyncClient() as client:\n    resp = await client.request(arguments['method'], arguments['url'], json=arguments.get('body'))\n    return resp.text",
                            "handler_language": "python",
                        }
                    ],
                },
            },
            {
                "id": uuid.UUID("00000000-0000-0000-0000-000000000002"),
                "name": "PostgreSQL Query",
                "description": "Read-only database access tool. Runs parameterized SELECT queries against a PostgreSQL database.",
                "category": "database",
                "is_public": True,
                "author_id": None,
                "use_count": 0,
                "config": {
                    "runtime": "python",
                    "transport": "stdio",
                    "tools": [
                        {
                            "name": "query_db",
                            "description": "Run a read-only SQL query and return results as JSON",
                            "input_schema": {
                                "type": "object",
                                "properties": {
                                    "sql": {"type": "string", "description": "SELECT query to run"},
                                    "params": {"type": "array", "description": "Query parameters", "items": {}},
                                },
                                "required": ["sql"],
                            },
                            "handler_code": "import asyncpg, os, json\nconn = await asyncpg.connect(os.environ['DATABASE_URL'])\nrows = await conn.fetch(arguments['sql'], *(arguments.get('params') or []))\nawait conn.close()\nreturn json.dumps([dict(r) for r in rows], default=str)",
                            "handler_language": "python",
                        }
                    ],
                },
            },
            {
                "id": uuid.UUID("00000000-0000-0000-0000-000000000003"),
                "name": "File System Access",
                "description": "Read files and list directories on the local filesystem. Useful for giving Claude access to project files.",
                "category": "filesystem",
                "is_public": True,
                "author_id": None,
                "use_count": 0,
                "config": {
                    "runtime": "python",
                    "transport": "stdio",
                    "tools": [
                        {
                            "name": "read_file",
                            "description": "Read the contents of a file",
                            "input_schema": {
                                "type": "object",
                                "properties": {
                                    "path": {"type": "string", "description": "Absolute or relative file path"},
                                },
                                "required": ["path"],
                            },
                            "handler_code": "from pathlib import Path\nreturn Path(arguments['path']).read_text(encoding='utf-8')",
                            "handler_language": "python",
                        },
                        {
                            "name": "list_directory",
                            "description": "List files and subdirectories at a path",
                            "input_schema": {
                                "type": "object",
                                "properties": {
                                    "path": {"type": "string", "description": "Directory path to list"},
                                },
                                "required": ["path"],
                            },
                            "handler_code": "import json\nfrom pathlib import Path\np = Path(arguments['path'])\nentries = [{'name': e.name, 'type': 'dir' if e.is_dir() else 'file', 'size': e.stat().st_size if e.is_file() else None} for e in sorted(p.iterdir())]\nreturn json.dumps(entries)",
                            "handler_language": "python",
                        },
                    ],
                },
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("deployments")
    op.drop_table("test_cases")
    op.drop_table("library_templates")
    op.drop_table("prompts")
    op.drop_table("resources")
    op.drop_table("tools")
    op.drop_table("projects")
