from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.content_asset import ContentAsset
from app.models.content_task import ContentTask
from app.models.project import Project
from app.models.publish_job import PublishJob
from app.models.topic_candidate import TopicCandidate
from app.schemas.dashboard import DashboardOverview


class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_project_overview(self, project_id: int) -> DashboardOverview:
        project = self.db.get(Project, project_id)
        if project is None:
            raise ValueError("project not found")

        topic_count = self._scalar_count(select(func.count(TopicCandidate.id)).where(TopicCandidate.project_id == project_id))
        content_task_count = self._scalar_count(select(func.count(ContentTask.id)).where(ContentTask.project_id == project_id))
        pending_review_count = self._scalar_count(
            select(func.count(ContentAsset.id))
            .join(ContentTask, ContentTask.id == ContentAsset.task_id)
            .where(ContentTask.project_id == project_id, ContentAsset.review_status == "pending_review")
        )
        approved_asset_count = self._scalar_count(
            select(func.count(ContentAsset.id))
            .join(ContentTask, ContentTask.id == ContentAsset.task_id)
            .where(ContentTask.project_id == project_id, ContentAsset.review_status == "approved")
        )
        publish_job_count = self._scalar_count(
            select(func.count(PublishJob.id)).join(ContentTask, ContentTask.id == PublishJob.task_id).where(ContentTask.project_id == project_id)
        )
        published_job_count = self._scalar_count(
            select(func.count(PublishJob.id))
            .join(ContentTask, ContentTask.id == PublishJob.task_id)
            .where(ContentTask.project_id == project_id, PublishJob.status == "success")
        )

        return DashboardOverview(
            project_id=project_id,
            project_name=project.name,
            topic_count=topic_count,
            content_task_count=content_task_count,
            pending_review_count=pending_review_count,
            approved_asset_count=approved_asset_count,
            publish_job_count=publish_job_count,
            published_job_count=published_job_count,
        )

    def _scalar_count(self, stmt) -> int:
        value = self.db.scalar(stmt)
        return int(value or 0)

