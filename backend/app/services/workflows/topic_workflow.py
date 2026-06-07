from sqlalchemy.orm import Session

from app.models.project import Project
from app.services.agents.topic_agent import TopicAgent
from app.services.llm.topic_service import TopicLLMService
from app.services.repositories.brand_profile_repo import BrandProfileRepository
from app.services.repositories.llm_log_repo import LLMLogRepository
from app.services.repositories.topic_repo import TopicRepository


class TopicWorkflowService:
    def __init__(self, db: Session):
        self.db = db
        self.brand_repo = BrandProfileRepository(db)
        self.topic_repo = TopicRepository(db)
        self.llm_log_repo = LLMLogRepository(db)
        self.topic_agent = TopicAgent(TopicLLMService(self.llm_log_repo))

    def run(self, project: Project) -> int:
        brand_profile = self.brand_repo.get_by_project_or_404(project.id)
        existing_titles = [item.title for item in self.topic_repo.list_by_project(project.id)]
        topics = self.topic_agent.generate_candidates(
            project_id=project.id,
            project_name=project.name,
            industry=project.industry,
            goal=project.goal,
            brand_name=brand_profile.brand_name,
            brand_desc=brand_profile.brand_desc,
            target_audience=brand_profile.target_audience,
            tone_of_voice=brand_profile.tone_of_voice,
            product_info=brand_profile.product_info_json,
            cta_rules=brand_profile.cta_rules_json,
            banned_words=brand_profile.banned_words_json,
            competitor_accounts=brand_profile.competitor_accounts_json,
            extra_context=brand_profile.extra_context,
            existing_titles=existing_titles,
        )
        payloads = [
            {
                "project_id": project.id,
                "title": item["title"],
                "angle": item["angle"],
                "source_type": item["source_type"],
                "source_payload_json": item["source_payload_json"],
                "heat_score": item["heat_score"],
                "relevance_score": item["relevance_score"],
                "conversion_score": item["conversion_score"],
                "competition_score": item["competition_score"],
                "final_score": item["final_score"],
                "reason": item["reason"],
                "status": "new",
            }
            for item in topics
        ]
        return len(self.topic_repo.bulk_create(payloads))
