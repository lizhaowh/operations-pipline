from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: ProjectCreate) -> Project:
        item = Project(**payload.model_dump())
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def list_all(self) -> list[Project]:
        return list(self.db.scalars(select(Project).order_by(Project.id.desc())))

    def get_or_404(self, project_id: int) -> Project:
        item = self.db.get(Project, project_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project not found")
        return item

    def update(self, project_id: int, payload: ProjectUpdate) -> Project:
        item = self.get_or_404(project_id)
        for key, value in payload.model_dump().items():
            setattr(item, key, value)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, project_id: int) -> None:
        item = self.get_or_404(project_id)
        self.db.delete(item)
        self.db.commit()
