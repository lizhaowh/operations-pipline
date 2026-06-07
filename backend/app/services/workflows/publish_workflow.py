from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.services.publishers.factory import PublisherFactory
from app.services.repositories.publish_repo import PublishRepository


class PublishWorkflowService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PublishRepository(db)

    def run(self, job_id: int):
        job = self.repo.get_job_or_404(job_id)
        asset = self.repo.get_asset_or_404(job.content_asset_id)
        if asset.review_status != "approved":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="content asset must be approved before publishing",
            )

        self.repo.mark_job_running(job)
        publisher = PublisherFactory.create(job.publish_mode)
        payload = publisher.build_payload(asset)
        return self.repo.mark_job_success(
            job,
            platform_post_id=payload.platform_post_id,
            post_url=payload.post_url,
            raw_response_json=payload.raw_response_json,
        )
