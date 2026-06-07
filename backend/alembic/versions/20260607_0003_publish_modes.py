"""publish modes"""

from alembic import op
import sqlalchemy as sa


revision = "20260607_0003"
down_revision = "20260607_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "publish_jobs",
        sa.Column("publish_mode", sa.String(length=32), nullable=False, server_default="manual_export"),
    )


def downgrade() -> None:
    op.drop_column("publish_jobs", "publish_mode")
