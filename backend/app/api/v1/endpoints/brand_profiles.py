from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.brand_profile import BrandProfileCreate, BrandProfileRead
from app.services.repositories.brand_profile_repo import BrandProfileRepository

router = APIRouter()


@router.post("", response_model=BrandProfileRead, status_code=status.HTTP_201_CREATED)
def create_brand_profile(payload: BrandProfileCreate, db: Session = Depends(get_db)) -> BrandProfileRead:
    item = BrandProfileRepository(db).upsert(payload)
    return BrandProfileRead.model_validate(item)


@router.get("/projects/{project_id}", response_model=BrandProfileRead)
def get_brand_profile(project_id: int, db: Session = Depends(get_db)) -> BrandProfileRead:
    item = BrandProfileRepository(db).get_by_project_or_404(project_id)
    return BrandProfileRead.model_validate(item)

