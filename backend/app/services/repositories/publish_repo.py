from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.content_asset import ContentAsset
from app.models.publish_job import PublishJob
from app.models.publish_result import PublishResult


class PublishRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_asset_or_404(self, asset_id: int) -> ContentAsset:
        item = self.db.get(ContentAsset, asset_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="content asset not found")
        return item

    def create_job(self, *, content_asset_id: int, publish_mode: str, scheduled_at: datetime | None) -> PublishJob:
        asset = self.get_asset_or_404(content_asset_id)
        job = PublishJob(
            task_id=asset.task_id,
            content_asset_id=asset.id,
            platform=asset.platform,
            publish_mode=publish_mode,
            status="scheduled" if scheduled_at else "draft",
            scheduled_at=scheduled_at,
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def get_job_or_404(self, job_id: int) -> PublishJob:
        item = self.db.get(PublishJob, job_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="publish job not found")
        return item

    def mark_job_running(self, job: PublishJob) -> PublishJob:
        job.status = "running"
        job.started_at = datetime.now(timezone.utc)
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def mark_job_success(
        self,
        job: PublishJob,
        *,
        platform_post_id: str | None,
        post_url: str | None,
        raw_response_json: dict,
    ) -> PublishResult:
        job.status = "success"
        job.finished_at = datetime.now(timezone.utc)
        self.db.add(job)
        result = PublishResult(
            publish_job_id=job.id,
            platform_post_id=platform_post_id,
            post_url=post_url,
            published_at=job.finished_at,
            raw_response_json=raw_response_json,
        )
        self.db.add(result)
        self.db.commit()
        self.db.refresh(job)
        self.db.refresh(result)
        return result

    def list_jobs_by_task(self, task_id: int) -> list[PublishJob]:
        stmt = select(PublishJob).where(PublishJob.task_id == task_id).order_by(PublishJob.id.asc())
        return list(self.db.scalars(stmt))

    def get_job_by_asset_id(self, asset_id: int) -> PublishJob | None:
        stmt = select(PublishJob).where(PublishJob.content_asset_id == asset_id).order_by(PublishJob.id.desc())
        return self.db.scalar(stmt)
