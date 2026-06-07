from app.services.llm.content_service import ContentLLMService
from app.services.repositories.llm_log_repo import LLMLogRepository


class WriterAgent:
    def __init__(self, llm_log_repo: LLMLogRepository):
        self.content_llm_service = ContentLLMService(llm_log_repo)

    def generate_bundle(self, *, project_id: int, topic_title: str, topic_angle: str | None, platform: str) -> dict:
        return self.content_llm_service.generate_article_bundle(
            project_id=project_id,
            topic_title=topic_title,
            topic_angle=topic_angle,
            platform=platform,
        )
