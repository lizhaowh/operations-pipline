import json
from time import perf_counter
from typing import Any

from app.core.config import get_settings
from app.services.llm.gateway import LLMGateway
from app.services.repositories.llm_log_repo import LLMLogRepository


class TopicLLMService:
    def __init__(self, llm_log_repo: LLMLogRepository):
        self.settings = get_settings()
        self.gateway = LLMGateway()
        self.llm_log_repo = llm_log_repo

    def generate_topics(
        self,
        *,
        project_id: int,
        project_name: str,
        industry: str | None,
        goal: str | None,
        brand_name: str,
        brand_desc: str | None,
        target_audience: str | None,
        tone_of_voice: str | None,
        product_info: dict | None,
        cta_rules: dict | None,
        banned_words: list[str] | None,
        competitor_accounts: list[dict] | None,
        extra_context: str | None,
        existing_titles: list[str],
    ) -> list[dict[str, Any]]:
        if not self.settings.dashscope_api_key:
            return []

        system_prompt = (
            "你是资深内容策略顾问。"
            "请基于品牌和项目上下文，生成适合内容增长和转化的中文选题。"
            "必须只输出严格 JSON，不要输出 markdown 代码块，不要附加解释。"
            "JSON 格式必须是对象，包含字段 topics。"
            "topics 是数组，长度为 8。"
            "每个元素必须包含字段：title, angle, heat_score, relevance_score, conversion_score, competition_score, reason。"
            "四个分数都必须是 0 到 100 的数字。"
            "title 要具体、可发布、避免空泛。"
            "angle 要说明切入角度和内容重点。"
            "reason 要简短说明为什么值得做。"
            "避免和 existing_titles 重复或近似。"
        )
        user_payload = {
            "project_name": project_name,
            "industry": industry,
            "goal": goal,
            "brand_name": brand_name,
            "brand_desc": brand_desc,
            "target_audience": target_audience,
            "tone_of_voice": tone_of_voice,
            "product_info_json": product_info,
            "cta_rules_json": cta_rules,
            "banned_words_json": banned_words,
            "competitor_accounts_json": competitor_accounts,
            "extra_context": extra_context,
            "existing_titles": existing_titles,
            "requirements": {
                "language": "zh-CN",
                "topic_count": 8,
                "focus": ["内容增长", "用户痛点", "转化相关", "可执行建议"],
            },
        }
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
        ]

        started = perf_counter()
        try:
            result = self.gateway.chat(messages, temperature=0.9)
            latency_ms = int((perf_counter() - started) * 1000)
            content = result["content"] or "{}"
            parsed = self._extract_topics(content)
            usage = result.get("usage")
            self.llm_log_repo.create(
                project_id=project_id,
                scene="topic_generation",
                model=self.gateway.model,
                request_payload_json={"messages": messages},
                response_text=content,
                prompt_tokens=getattr(usage, "prompt_tokens", None),
                completion_tokens=getattr(usage, "completion_tokens", None),
                latency_ms=latency_ms,
                status="success",
                error_message=None,
            )
            return parsed
        except Exception as exc:
            latency_ms = int((perf_counter() - started) * 1000)
            self.llm_log_repo.create(
                project_id=project_id,
                scene="topic_generation",
                model=self.gateway.model,
                request_payload_json={"messages": messages},
                response_text=None,
                prompt_tokens=None,
                completion_tokens=None,
                latency_ms=latency_ms,
                status="failed",
                error_message=str(exc),
            )
            return []

    def _extract_topics(self, content: str) -> list[dict[str, Any]]:
        normalized = content.strip()
        if normalized.startswith("```"):
            lines = normalized.splitlines()
            if len(lines) >= 3:
                normalized = "\n".join(lines[1:-1]).strip()
        parsed = json.loads(normalized)
        topics = parsed.get("topics", [])
        if not isinstance(topics, list):
            raise ValueError("topics field must be a list")
        return [item for item in topics if isinstance(item, dict)]
