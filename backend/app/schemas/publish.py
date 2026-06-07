from datetime import datetime

from pydantic import BaseModel


class PublishJobCreate(BaseModel):
    content_asset_id: int
    publish_mode: str = "manual_export"
    scheduled_at: datetime | None = None


class PublishJobRead(BaseModel):
    id: int
    task_id: int
    content_asset_id: int
    platform: str
    publish_mode: str
    status: str
    scheduled_at: datetime | None
    started_at: datetime | None
    finished_at: datetime | None
    retry_count: int
    last_error: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PublishResultRead(BaseModel):
    id: int
    publish_job_id: int
    platform_post_id: str | None
    post_url: str | None
    published_at: datetime | None
    raw_response_json: dict | None
    created_at: datetime

    model_config = {"from_attributes": True}


class PublishExecutionCheckRead(BaseModel):
    ok: bool
    code: str
    message: str


class PublishExecutionPreviewRead(BaseModel):
    platform: str
    can_run: bool
    launch_mode: str
    start_url: str | None
    storage_state_path: str | None
    selectors: dict[str, str]
    checks: list[PublishExecutionCheckRead]
    steps: list[str]
    notes: list[str]
    payload_summary: dict


class PublishExecutionRunRead(BaseModel):
    status: str
    reason: str | None = None
    platform: str | None = None
    start_url: str | None = None
    next_action: str | None = None
    checks: list[PublishExecutionCheckRead] | None = None
    filled_fields: dict | None = None
