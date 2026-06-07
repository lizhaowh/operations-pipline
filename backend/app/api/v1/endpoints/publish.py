from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.publish import (
    PublishExecutionRunRead,
    PublishExecutionPreviewRead,
    PublishJobCreate,
    PublishJobRead,
    PublishResultRead,
)
from app.services.publishers.assist_preview_service import AssistedPublishPreviewService
from app.services.repositories.publish_repo import PublishRepository
from app.services.workflows.publish_workflow import PublishWorkflowService

router = APIRouter()


@router.post("/jobs", response_model=PublishJobRead, status_code=status.HTTP_201_CREATED)
def create_publish_job(payload: PublishJobCreate, db: Session = Depends(get_db)) -> PublishJobRead:
    job = PublishRepository(db).create_job(
        content_asset_id=payload.content_asset_id,
        publish_mode=payload.publish_mode,
        scheduled_at=payload.scheduled_at,
    )
    return PublishJobRead.model_validate(job)


@router.post("/jobs/{job_id}/run", response_model=PublishResultRead)
def run_publish_job(job_id: int, db: Session = Depends(get_db)) -> PublishResultRead:
    result = PublishWorkflowService(db).run(job_id)
    return PublishResultRead.model_validate(result)


@router.get("/jobs/{job_id}", response_model=PublishJobRead)
def get_publish_job(job_id: int, db: Session = Depends(get_db)) -> PublishJobRead:
    job = PublishRepository(db).get_job_or_404(job_id)
    return PublishJobRead.model_validate(job)


@router.get("/assets/{asset_id}/assist-preview", response_model=PublishExecutionPreviewRead)
def get_assisted_publish_preview(asset_id: int, db: Session = Depends(get_db)) -> PublishExecutionPreviewRead:
    asset = PublishRepository(db).get_asset_or_404(asset_id)
    try:
        preview = AssistedPublishPreviewService().build_preview(asset=asset)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return PublishExecutionPreviewRead(
        platform=preview.platform,
        can_run=preview.can_run,
        launch_mode=preview.launch_mode,
        start_url=preview.start_url,
        storage_state_path=preview.storage_state_path,
        selectors=preview.selectors,
        checks=[{"ok": item.ok, "code": item.code, "message": item.message} for item in preview.checks],
        steps=preview.steps,
        notes=preview.notes,
        payload_summary=preview.payload_summary,
    )


@router.post("/assets/{asset_id}/assist-run", response_model=PublishExecutionRunRead)
async def run_assisted_publish_execution(asset_id: int, db: Session = Depends(get_db)) -> PublishExecutionRunRead:
    asset = PublishRepository(db).get_asset_or_404(asset_id)
    try:
        result = await AssistedPublishPreviewService().execute_until_publish_confirmation(asset=asset)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return PublishExecutionRunRead.model_validate(result)
