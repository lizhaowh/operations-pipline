from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.topic_candidate import TopicCandidate


class TopicRepository:
    def __init__(self, db: Session):
        self.db = db

    def bulk_create(self, payloads: list[dict]) -> list[TopicCandidate]:
        items = [TopicCandidate(**payload) for payload in payloads]
        self.db.add_all(items)
        self.db.commit()
        for item in items:
            self.db.refresh(item)
        return items

    def list_by_project(self, project_id: int) -> list[TopicCandidate]:
        stmt = select(TopicCandidate).where(TopicCandidate.project_id == project_id).order_by(TopicCandidate.final_score.desc())
        return list(self.db.scalars(stmt))

    def get_by_project_or_404(self, project_id: int, topic_id: int) -> TopicCandidate:
        stmt = select(TopicCandidate).where(
            TopicCandidate.project_id == project_id,
            TopicCandidate.id == topic_id,
        )
        item = self.db.scalar(stmt)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="topic not found")
        return item

    def delete(self, project_id: int, topic_id: int) -> None:
        item = self.get_by_project_or_404(project_id, topic_id)
        self.db.delete(item)
        self.db.commit()
