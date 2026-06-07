from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.media import MediaAssetRead, MediaGenerateRequest
from app.services.repositories.media_repo import MediaRepository

router = APIRouter()


@router.get("/projects/{project_id}", response_model=list[MediaAssetRead])
def list_project_media_assets(project_id: int, db: Session = Depends(get_db)) -> list[MediaAssetRead]:
    items = MediaRepository(db).list_by_project(project_id)
    return [MediaAssetRead.model_validate(item) for item in items]


@router.get("/tasks/{task_id}", response_model=list[MediaAssetRead])
def list_task_media_assets(task_id: int, db: Session = Depends(get_db)) -> list[MediaAssetRead]:
    items = MediaRepository(db).list_by_task(task_id)
    return [MediaAssetRead.model_validate(item) for item in items]


@router.post(
    "/content-assets/{content_asset_id}/generate",
    response_model=list[MediaAssetRead],
    status_code=status.HTTP_201_CREATED,
)
def generate_demo_media_assets(
    content_asset_id: int,
    payload: MediaGenerateRequest,
    db: Session = Depends(get_db),
) -> list[MediaAssetRead]:
    items = MediaRepository(db).create_demo_media_for_asset(content_asset_id, payload.roles)
    return [MediaAssetRead.model_validate(item) for item in items]
