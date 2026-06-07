from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class TopicCandidate(Base):
    __tablename__ = "topic_candidates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    angle: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_type: Mapped[str] = mapped_column(String(32), nullable=False)
    source_payload_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    heat_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    relevance_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    conversion_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    competition_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    final_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="new", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

