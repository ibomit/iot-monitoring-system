"""Add measurements lookup index

Revision ID: b3f7a1c9d2e4
Revises: 8e4d9c1f2a7b
Create Date: 2026-10-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = "b3f7a1c9d2e4"
down_revision: Union[str, Sequence[str], None] = "8e4d9c1f2a7b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_measurements_sensor_metric_created_at",
        "measurements",
        ["sensor_id", "metric", "created_at"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_measurements_sensor_metric_created_at",
        table_name="measurements",
    )
