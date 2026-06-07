from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ContentGenerateRequest(BaseModel):
    topic_id: int
    platforms: list[str] = Field(default_factory=lambda: ["wechat", "xiaohongshu"])


class ContentTaskRead(BaseModel):
    id: int
    project_id: int
    topic_id: int
    workflow_type: str
    status: str
    scheduled_at: datetime | None
    approved_at: datetime | None
    published_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ContentTaskDetail(BaseModel):
    task: ContentTaskRead
    assets: list["ContentAssetRead"]


class ContentAssetRead(BaseModel):
    id: int
    task_id: int
    platform: str
    asset_type: str
    title: str | None
    outline_json: dict[str, Any] | list[Any] | None
    content_markdown: str | None
    summary: str | None
    tags_json: list[str] | None
    cover_text: str | None
    cta_text: str | None
    version: int
    review_status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


ContentTaskDetail.model_rebuild()
