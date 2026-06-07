from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class PublishResult(Base):
    __tablename__ = "publish_results"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    publish_job_id: Mapped[int] = mapped_column(ForeignKey("publish_jobs.id", ondelete="CASCADE"), nullable=False, unique=True)
    platform_post_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    post_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    raw_response_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

