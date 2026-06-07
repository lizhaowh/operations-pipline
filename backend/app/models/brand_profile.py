from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class BrandProfile(Base):
    __tablename__ = "brand_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True)
    brand_name: Mapped[str] = mapped_column(String(128), nullable=False)
    brand_desc: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_audience: Mapped[str | None] = mapped_column(Text, nullable=True)
    tone_of_voice: Mapped[str | None] = mapped_column(String(64), nullable=True)
    product_info_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    cta_rules_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    banned_words_json: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    competitor_accounts_json: Mapped[list[dict] | None] = mapped_column(JSON, nullable=True)
    extra_context: Mapped[str | None] = mapped_column(Text, nullable=True)

