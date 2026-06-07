from typing import Any

from pydantic import BaseModel, Field, field_validator


def _normalize_competitor_account(item: Any) -> dict[str, Any]:
    if isinstance(item, dict):
        return item
    if isinstance(item, str):
        return {"name": item}
    raise TypeError("competitor_accounts_json items must be objects or strings")


class BrandProfileCreate(BaseModel):
    project_id: int
    brand_name: str = Field(min_length=2, max_length=128)
    brand_desc: str | None = None
    target_audience: str | None = None
    tone_of_voice: str | None = Field(default=None, max_length=64)
    product_info_json: dict | None = None
    cta_rules_json: dict | None = None
    banned_words_json: list[str] | None = None
    competitor_accounts_json: list[dict] | None = None
    extra_context: str | None = None

    @field_validator("competitor_accounts_json", mode="before")
    @classmethod
    def normalize_competitor_accounts(cls, value: Any) -> Any:
        if value is None:
            return None
        if not isinstance(value, list):
            return value
        return [_normalize_competitor_account(item) for item in value]


class BrandProfileRead(BrandProfileCreate):
    id: int

    model_config = {"from_attributes": True}
