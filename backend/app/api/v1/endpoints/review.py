from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.content import ContentAssetRead
from app.schemas.review import ReviewRequest
from app.services.repositories.content_repo import ContentRepository

router = APIRouter()


@router.post("/assets/{asset_id}", response_model=ContentAssetRead)
def review_asset(asset_id: int, payload: ReviewRequest, db: Session = Depends(get_db)) -> ContentAssetRead:
    item = ContentRepository(db).review_asset(asset_id=asset_id, approved=payload.approved, notes=payload.notes)
    return ContentAssetRead.model_validate(item)

