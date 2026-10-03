"""Make timestamps timezone-aware

Existing values were written by Python's datetime.now() in the developer
machine's local time (Europe/Berlin), so they are converted from that zone.
New values are stored as UTC.

Revision ID: c5d8e2f4a6b1
Revises: b3f7a1c9d2e4
Create Date: 2026-10-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c5d8e2f4a6b1"
down_revision: Union[str, Sequence[str], None] = "b3f7a1c9d2e4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SOURCE_TIMEZONE = "Europe/Berlin"

COLUMNS = [
    ("devices", "created_at"),
    ("devices", "last_seen_at"),
    ("sensors", "created_at"),
    ("measurements", "created_at"),
    ("users", "created_at"),
]


def upgrade() -> None:
    for table, column in COLUMNS:
        op.alter_column(
            table,
            column,
            type_=sa.DateTime(timezone=True),
            existing_type=sa.DateTime(),
            postgresql_using=f"{column} AT TIME ZONE '{SOURCE_TIMEZONE}'",
        )


def downgrade() -> None:
    for table, column in COLUMNS:
        op.alter_column(
            table,
            column,
            type_=sa.DateTime(),
            existing_type=sa.DateTime(timezone=True),
            postgresql_using=f"{column} AT TIME ZONE '{SOURCE_TIMEZONE}'",
        )
