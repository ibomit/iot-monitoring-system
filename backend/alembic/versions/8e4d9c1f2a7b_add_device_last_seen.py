"""Add device liveness timestamp

Revision ID: 8e4d9c1f2a7b
Revises: fdc8daaf30a5
Create Date: 2026-09-20 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8e4d9c1f2a7b"
down_revision: Union[str, Sequence[str], None] = "fdc8daaf30a5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "devices",
        sa.Column("last_seen_at", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("devices", "last_seen_at")
