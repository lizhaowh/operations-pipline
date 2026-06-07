from datetime import datetime

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=128)
    industry: str | None = Field(default=None, max_length=64)
    goal: str | None = None


class ProjectUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=128)
    industry: str | None = Field(default=None, max_length=64)
    goal: str | None = None


class ProjectRead(BaseModel):
    id: int
    name: str
    industry: str | None
    goal: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
