from datetime import datetime

from pydantic import BaseModel


class TopicRead(BaseModel):
    id: int
    project_id: int
    title: str
    angle: str | None
    source_type: str
    heat_score: float
    relevance_score: float
    conversion_score: float
    competition_score: float
    final_score: float
    reason: str | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}

