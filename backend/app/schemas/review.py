from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    approved: bool = Field(description="Whether the asset is approved for publishing")
    notes: str | None = Field(default=None, max_length=1000)

