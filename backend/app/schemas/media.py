from datetime import datetime
from typing import Any

from pydantic import BaseModel


class MediaGenerateRequest(BaseModel):
    roles: list[str] = ["cover", "body"]


class MediaAssetRead(BaseModel):
    id: int
    task_id: int
    content_asset_id: int | None
    platform: str
    media_type: str
    role: str
    title: str | None
    prompt_text: str | None
    file_url: str | None
    file_path: str | None
    status: str
    metadata_json: dict[str, Any] | list[Any] | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
