from sqlalchemy.orm import Session

from app.schemas.content import ContentGenerateRequest
from app.services.agents.writer_agent import WriterAgent
from app.services.repositories.content_repo import ContentRepository
from app.services.repositories.llm_log_repo import LLMLogRepository


class ContentWorkflowService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ContentRepository(db)
        self.writer_agent = WriterAgent(LLMLogRepository(db))

    def run(self, payload: ContentGenerateRequest):
        topic = self.repo.get_topic_or_404(payload.topic_id)
        task = self.repo.create_task(project_id=topic.project_id, topic_id=topic.id)
        self.repo.update_task_status(task, "outline_generated")

        for platform in payload.platforms:
            bundle = self.writer_agent.generate_bundle(
                project_id=topic.project_id,
                topic_title=topic.title,
                topic_angle=topic.angle,
                platform=platform,
            )
            self.repo.create_asset(
                task_id=task.id,
                platform=platform,
                asset_type="article",
                title=bundle["title"],
                outline_json=bundle["outline_json"],
                content_markdown=bundle["content_markdown"],
                summary=bundle["summary"],
                tags_json=bundle["tags_json"],
                cover_text=bundle["cover_text"],
                cta_text=bundle["cta_text"],
            )

        return self.repo.update_task_status(task, "pending_review")

