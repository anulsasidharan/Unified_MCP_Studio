"""Projects, tools, resources, prompts, templates, test_cases, deployments.

Revision ID: 20260514_0002
Revises: 20260513_0001
Create Date: 2026-05-14

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260514_0002"
down_revision: Union[str, Sequence[str], None] = "20260513_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("runtime", sa.String(length=50), nullable=False),
        sa.Column("transport", sa.String(length=50), nullable=False),
        sa.Column(
            "config",
            postgresql.JSONB(astext_type=sa.Text()),
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
    op.create_index(op.f("ix_projects_user_id"), "projects", ["user_id"], unique=False)

    op.create_table(
        "templates",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column(
            "is_public",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column("author_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("use_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("config", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
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
    op.create_index(op.f("ix_templates_category"), "templates", ["category"], unique=False)

    op.create_table(
        "tools",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("input_schema", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("handler_code", sa.Text(), nullable=False),
        sa.Column("handler_language", sa.String(length=50), nullable=False),
        sa.Column(
            "metadata",
            postgresql.JSONB(astext_type=sa.Text()),
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
    op.create_index(op.f("ix_tools_project_id"), "tools", ["project_id"], unique=False)

    op.create_table(
        "resources",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("uri", sa.String(length=500), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("mime_type", sa.String(length=100), nullable=True),
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
    op.create_index(op.f("ix_resources_project_id"), "resources", ["project_id"], unique=False)

    op.create_table(
        "prompts",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "arguments",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "messages",
            postgresql.JSONB(astext_type=sa.Text()),
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
    op.create_index(op.f("ix_prompts_project_id"), "prompts", ["project_id"], unique=False)

    op.create_table(
        "deployments",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("target", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("url", sa.String(length=500), nullable=True),
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
    op.create_index(
        op.f("ix_deployments_project_id"),
        "deployments",
        ["project_id"],
        unique=False,
    )

    op.create_table(
        "test_cases",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("tool_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("input_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("expected_output", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["tool_id"], ["tools.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_test_cases_tool_id"), "test_cases", ["tool_id"], unique=False)

    templates_tbl = sa.table(
        "templates",
        sa.column("name", sa.String()),
        sa.column("description", sa.Text()),
        sa.column("category", sa.String()),
        sa.column("is_public", sa.Boolean()),
        sa.column("author_id", postgresql.UUID(as_uuid=True)),
        sa.column("use_count", sa.Integer()),
        sa.column("config", postgresql.JSONB(astext_type=sa.Text())),
    )
    op.bulk_insert(
        templates_tbl,
        [
            {
                "name": "Minimal Python MCP",
                "description": "Single-tool Python MCP server (stdio) — starting point.",
                "category": "starter",
                "is_public": True,
                "author_id": None,
                "use_count": 0,
                "config": {
                    "runtime": "python",
                    "transport": "stdio",
                    "project": {"name": "From template", "description": "Minimal MCP"},
                    "tools": [
                        {
                            "name": "hello",
                            "description": "Returns a greeting",
                            "input_schema": {
                                "type": "object",
                                "properties": {"name": {"type": "string"}},
                                "additionalProperties": False,
                            },
                            "handler_code": (
                                '    name = arguments.get("name", "world")\n'
                                '    return {"message": f"Hello, {name}!"}\n'
                            ),
                            "handler_language": "python",
                        }
                    ],
                    "resources": [],
                    "prompts": [],
                },
            },
            {
                "name": "Minimal TypeScript MCP",
                "description": "Single-tool TypeScript MCP server (stdio) — starting point.",
                "category": "starter",
                "is_public": True,
                "author_id": None,
                "use_count": 0,
                "config": {
                    "runtime": "typescript",
                    "transport": "stdio",
                    "project": {"name": "From template", "description": "Minimal MCP"},
                    "tools": [
                        {
                            "name": "hello",
                            "description": "Returns a greeting",
                            "input_schema": {
                                "type": "object",
                                "properties": {"name": {"type": "string"}},
                                "additionalProperties": False,
                            },
                            "handler_code": (
                                '  const name = (arguments as any).name ?? "world";\n'
                                "  return { message: `Hello, ${name}!` };\n"
                            ),
                            "handler_language": "typescript",
                        }
                    ],
                    "resources": [],
                    "prompts": [],
                },
            },
        ],
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_test_cases_tool_id"), table_name="test_cases")
    op.drop_table("test_cases")
    op.drop_index(op.f("ix_deployments_project_id"), table_name="deployments")
    op.drop_table("deployments")
    op.drop_index(op.f("ix_prompts_project_id"), table_name="prompts")
    op.drop_table("prompts")
    op.drop_index(op.f("ix_resources_project_id"), table_name="resources")
    op.drop_table("resources")
    op.drop_index(op.f("ix_tools_project_id"), table_name="tools")
    op.drop_table("tools")
    op.drop_index(op.f("ix_templates_category"), table_name="templates")
    op.drop_table("templates")
    op.drop_index(op.f("ix_projects_user_id"), table_name="projects")
    op.drop_table("projects")
