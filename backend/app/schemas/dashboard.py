from pydantic import BaseModel


class DashboardOverview(BaseModel):
    project_id: int
    project_name: str
    topic_count: int
    content_task_count: int
    pending_review_count: int
    approved_asset_count: int
    publish_job_count: int
    published_job_count: int

