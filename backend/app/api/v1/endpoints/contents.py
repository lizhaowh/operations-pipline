from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.content import ContentAssetRead, ContentGenerateRequest, ContentTaskDetail, ContentTaskRead
from app.services.repositories.content_repo import ContentRepository
from app.services.workflows.content_workflow import ContentWorkflowService

router = APIRouter()


@router.post("/generate", response_model=ContentTaskRead, status_code=status.HTTP_201_CREATED)
def generate_content(payload: ContentGenerateRequest, db: Session = Depends(get_db)) -> ContentTaskRead:
    task = ContentWorkflowService(db).run(payload)
    return ContentTaskRead.model_validate(task)


@router.get("/tasks/{task_id}", response_model=ContentTaskRead)
def get_content_task(task_id: int, db: Session = Depends(get_db)) -> ContentTaskRead:
    task = ContentRepository(db).get_task_or_404(task_id)
    return ContentTaskRead.model_validate(task)


@router.get("/projects/{project_id}/tasks", response_model=list[ContentTaskRead])
def list_project_content_tasks(project_id: int, db: Session = Depends(get_db)) -> list[ContentTaskRead]:
    items = ContentRepository(db).list_tasks_by_project(project_id)
    return [ContentTaskRead.model_validate(item) for item in items]


@router.get("/tasks/{task_id}/assets", response_model=list[ContentAssetRead])
def list_content_assets(task_id: int, db: Session = Depends(get_db)) -> list[ContentAssetRead]:
    items = ContentRepository(db).list_assets_by_task(task_id)
    return [ContentAssetRead.model_validate(item) for item in items]


@router.get("/tasks/{task_id}/detail", response_model=ContentTaskDetail)
def get_content_task_detail(task_id: int, db: Session = Depends(get_db)) -> ContentTaskDetail:
    repo = ContentRepository(db)
    task = repo.get_task_or_404(task_id)
    assets = repo.list_assets_by_task(task_id)
    return ContentTaskDetail(
        task=ContentTaskRead.model_validate(task),
        assets=[ContentAssetRead.model_validate(item) for item in assets],
    )
