"""media assets"""

from alembic import op
import sqlalchemy as sa


revision = "20260607_0004"
down_revision = "20260607_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "media_assets",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("content_asset_id", sa.Integer(), nullable=True),
        sa.Column("platform", sa.String(length=32), nullable=False),
        sa.Column("media_type", sa.String(length=32), nullable=False, server_default="image"),
        sa.Column("role", sa.String(length=32), nullable=False, server_default="cover"),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("prompt_text", sa.Text(), nullable=True),
        sa.Column("file_url", sa.Text(), nullable=True),
        sa.Column("file_path", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="generated"),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["content_asset_id"], ["content_assets.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["task_id"], ["content_tasks.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_media_assets_task_id"), "media_assets", ["task_id"], unique=False)
    op.create_index(op.f("ix_media_assets_content_asset_id"), "media_assets", ["content_asset_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_media_assets_content_asset_id"), table_name="media_assets")
    op.drop_index(op.f("ix_media_assets_task_id"), table_name="media_assets")
    op.drop_table("media_assets")
