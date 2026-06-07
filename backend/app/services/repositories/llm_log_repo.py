from sqlalchemy.orm import Session

from app.models.llm_call_log import LLMCallLog


class LLMLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        project_id: int | None,
        scene: str,
        model: str,
        request_payload_json: dict | None,
        response_text: str | None,
        prompt_tokens: int | None,
        completion_tokens: int | None,
        latency_ms: int | None,
        status: str,
        error_message: str | None,
    ) -> LLMCallLog:
        item = LLMCallLog(
            project_id=project_id,
            scene=scene,
            model=model,
            request_payload_json=request_payload_json,
            response_text=response_text,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            latency_ms=latency_ms,
            status=status,
            error_message=error_message,
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

