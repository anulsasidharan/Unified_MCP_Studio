"""Rename legacy `templates` table to `library_templates` if needed.

Revision ID: 20260515_0003
Revises: 20260514_0002
Create Date: 2026-05-15

Some databases applied an earlier revision of 20260514_0002 that created `templates`
instead of `library_templates`. The ORM and API expect `library_templates`.
This revision aligns the physical table name without dropping data.
"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import inspect, text

revision: str = "20260515_0003"
down_revision: Union[str, Sequence[str], None] = "20260514_0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    insp = inspect(bind)
    names = set(insp.get_table_names())
    if "library_templates" in names:
        return
    if "templates" in names:
        op.rename_table("templates", "library_templates")
        # Optional: normalize index name to match fresh installs from 20260514_0002
        bind.execute(
            text(
                "ALTER INDEX IF EXISTS ix_templates_category "
                "RENAME TO idx_library_templates_category"
            )
        )


def downgrade() -> None:
    bind = op.get_bind()
    insp = inspect(bind)
    names = set(insp.get_table_names())
    if "templates" in names:
        return
    if "library_templates" in names:
        bind.execute(
            text(
                "ALTER INDEX IF EXISTS idx_library_templates_category "
                "RENAME TO ix_templates_category"
            )
        )
        op.rename_table("library_templates", "templates")
