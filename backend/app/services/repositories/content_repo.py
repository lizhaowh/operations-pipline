from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.content_asset import ContentAsset
from app.models.content_task import ContentTask
from app.models.topic_candidate import TopicCandidate


class ContentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_topic_or_404(self, topic_id: int) -> TopicCandidate:
        item = self.db.get(TopicCandidate, topic_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="topic not found")
        return item

    def create_task(self, *, project_id: int, topic_id: int, workflow_type: str = "article_generation") -> ContentTask:
        task = ContentTask(
            project_id=project_id,
            topic_id=topic_id,
            workflow_type=workflow_type,
            status="draft_requested",
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update_task_status(self, task: ContentTask, status_value: str) -> ContentTask:
        task.status = status_value
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_task_or_404(self, task_id: int) -> ContentTask:
        item = self.db.get(ContentTask, task_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="content task not found")
        return item

    def list_tasks_by_project(self, project_id: int) -> list[ContentTask]:
        stmt = select(ContentTask).where(ContentTask.project_id == project_id).order_by(ContentTask.id.desc())
        return list(self.db.scalars(stmt))

    def create_asset(
        self,
        *,
        task_id: int,
        platform: str,
        asset_type: str,
        title: str | None,
        outline_json: dict[str, Any] | list[Any] | None,
        content_markdown: str | None,
        summary: str | None,
        tags_json: list[str] | None,
        cover_text: str | None,
        cta_text: str | None,
    ) -> ContentAsset:
        item = ContentAsset(
            task_id=task_id,
            platform=platform,
            asset_type=asset_type,
            title=title,
            outline_json=outline_json,
            content_markdown=content_markdown,
            summary=summary,
            tags_json=tags_json,
            cover_text=cover_text,
            cta_text=cta_text,
            review_status="pending_review",
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def list_assets_by_task(self, task_id: int) -> list[ContentAsset]:
        stmt = select(ContentAsset).where(ContentAsset.task_id == task_id).order_by(ContentAsset.id.asc())
        return list(self.db.scalars(stmt))

    def sync_task_status_from_assets(self, task: ContentTask) -> ContentTask:
        assets = self.list_assets_by_task(task.id)
        statuses = {asset.review_status for asset in assets}

        if assets and statuses == {"approved"}:
            task.status = "approved"
        elif "rejected" in statuses:
            task.status = "rejected"
        else:
            task.status = "pending_review"

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def review_asset(self, *, asset_id: int, approved: bool, notes: str | None) -> ContentAsset:
        item = self.db.get(ContentAsset, asset_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="content asset not found")
        item.review_status = "approved" if approved else "rejected"
        if notes:
            item.summary = f"{item.summary or ''}\n\nReview Notes: {notes}".strip()
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        task = self.get_task_or_404(item.task_id)
        self.sync_task_status_from_assets(task)
        return item
