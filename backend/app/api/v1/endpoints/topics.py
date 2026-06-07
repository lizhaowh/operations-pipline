from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.topic import TopicRead
from app.services.repositories.project_repo import ProjectRepository
from app.services.repositories.topic_repo import TopicRepository
from app.services.workflows.topic_workflow import TopicWorkflowService

router = APIRouter()


@router.post("/projects/{project_id}/generate", status_code=status.HTTP_202_ACCEPTED)
def generate_topics(project_id: int, db: Session = Depends(get_db)) -> dict[str, int | str]:
    project = ProjectRepository(db).get_or_404(project_id)
    count = TopicWorkflowService(db).run(project)
    return {"message": "topic generation completed", "project_id": project_id, "count": count}


@router.get("/projects/{project_id}", response_model=list[TopicRead])
def list_topics(project_id: int, db: Session = Depends(get_db)) -> list[TopicRead]:
    items = TopicRepository(db).list_by_project(project_id)
    return [TopicRead.model_validate(item) for item in items]


@router.delete("/projects/{project_id}/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_topic(project_id: int, topic_id: int, db: Session = Depends(get_db)) -> None:
    TopicRepository(db).delete(project_id, topic_id)
