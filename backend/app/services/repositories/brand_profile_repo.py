from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.brand_profile import BrandProfile
from app.schemas.brand_profile import BrandProfileCreate
from app.services.repositories.project_repo import ProjectRepository


class BrandProfileRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert(self, payload: BrandProfileCreate) -> BrandProfile:
        ProjectRepository(self.db).get_or_404(payload.project_id)
        existing = self.db.scalar(select(BrandProfile).where(BrandProfile.project_id == payload.project_id))
        if existing is None:
            existing = BrandProfile(**payload.model_dump())
            self.db.add(existing)
        else:
            for key, value in payload.model_dump().items():
                setattr(existing, key, value)
        self.db.commit()
        self.db.refresh(existing)
        return existing

    def get_by_project_or_404(self, project_id: int) -> BrandProfile:
        item = self.db.scalar(select(BrandProfile).where(BrandProfile.project_id == project_id))
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="brand profile not found")
        return item

