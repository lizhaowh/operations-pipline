from typing import Any

from app.services.llm.topic_service import TopicLLMService


class TopicAgent:
    def __init__(self, topic_llm_service: TopicLLMService):
        self.topic_llm_service = topic_llm_service

    def generate_candidates(
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
        generated = self.topic_llm_service.generate_topics(
            project_id=project_id,
            project_name=project_name,
            industry=industry,
            goal=goal,
            brand_name=brand_name,
            brand_desc=brand_desc,
            target_audience=target_audience,
            tone_of_voice=tone_of_voice,
            product_info=product_info,
            cta_rules=cta_rules,
            banned_words=banned_words,
            competitor_accounts=competitor_accounts,
            extra_context=extra_context,
            existing_titles=existing_titles,
        )
        normalized = self._normalize_generated_topics(
            generated,
            project_name=project_name,
            brand_name=brand_name,
            target_audience=target_audience,
            goal=goal,
            existing_titles=existing_titles,
        )
        if normalized:
            return normalized
        return self._fallback_candidates(
            project_name=project_name,
            industry=industry,
            goal=goal,
            brand_name=brand_name,
            target_audience=target_audience,
            tone_of_voice=tone_of_voice,
            existing_titles=existing_titles,
        )

    def _normalize_generated_topics(
        self,
        generated: list[dict[str, Any]],
        *,
        project_name: str,
        brand_name: str,
        target_audience: str | None,
        goal: str | None,
        existing_titles: list[str],
    ) -> list[dict[str, Any]]:
        seen_titles = {self._title_key(title) for title in existing_titles}
        normalized: list[dict[str, Any]] = []
        for item in generated:
            title = str(item.get("title", "")).strip()
            if not title:
                continue
            title_key = self._title_key(title)
            if title_key in seen_titles:
                continue
            angle = str(item.get("angle", "")).strip() or None
            heat_score = self._clamp_score(item.get("heat_score"))
            relevance_score = self._clamp_score(item.get("relevance_score"))
            conversion_score = self._clamp_score(item.get("conversion_score"))
            competition_score = self._clamp_score(item.get("competition_score"))
            final_score = round(
                (heat_score * 0.25)
                + (relevance_score * 0.35)
                + (conversion_score * 0.30)
                - (competition_score * 0.10),
                2,
            )
            normalized.append(
                {
                    "title": title,
                    "angle": angle,
                    "source_type": "llm_generated",
                    "source_payload_json": {"project_name": project_name, "generator": "topic_llm_service"},
                    "heat_score": heat_score,
                    "relevance_score": relevance_score,
                    "conversion_score": conversion_score,
                    "competition_score": competition_score,
                    "final_score": final_score,
                    "reason": str(item.get("reason", "")).strip()
                    or f"贴合 {brand_name} 面向 {target_audience or '目标用户'} 的内容目标，且与“{goal or '内容增长'}”相关。",
                }
            )
            seen_titles.add(title_key)
        return normalized

    def _fallback_candidates(
        self,
        *,
        project_name: str,
        industry: str | None,
        goal: str | None,
        brand_name: str,
        target_audience: str | None,
        tone_of_voice: str | None,
        existing_titles: list[str],
    ) -> list[dict[str, Any]]:
        audience = target_audience or "泛行业用户"
        voice = tone_of_voice or "专业、清晰"
        base_industry = industry or "通用行业"
        base_goal = goal or "提升内容产能和转化"
        seeds = [
            f"{brand_name} 在 {base_industry} 里最容易被忽视的增长机会",
            f"{audience} 最常见的 5 个决策误区",
            "为什么很多团队做内容却拿不到稳定线索",
            "从 0 到 1 建立内容生产系统的关键步骤",
            f"{base_industry} 内容选题如何兼顾流量和转化",
        ]

        seen_titles = {self._title_key(title) for title in existing_titles}
        topics: list[dict[str, Any]] = []
        for index, title in enumerate(seeds, start=1):
            title_key = self._title_key(title)
            if title_key in seen_titles:
                continue
            heat_score = min(90, 60 + index * 4)
            relevance_score = min(95, 70 + index * 3)
            conversion_score = min(92, 68 + index * 4)
            competition_score = max(20, 55 - index * 3)
            final_score = round(
                (heat_score * 0.25)
                + (relevance_score * 0.35)
                + (conversion_score * 0.3)
                - (competition_score * 0.1),
                2,
            )
            topics.append(
                {
                    "title": title,
                    "angle": f"用 {voice} 的表达方式，围绕“{base_goal}”给出可执行建议",
                    "source_type": "seed_template",
                    "source_payload_json": {"seed_index": index, "project_name": project_name},
                    "heat_score": float(heat_score),
                    "relevance_score": float(relevance_score),
                    "conversion_score": float(conversion_score),
                    "competition_score": float(competition_score),
                    "final_score": float(final_score),
                    "reason": f"贴合 {brand_name} 的目标用户 {audience}，适合作为第一版验证选题。",
                }
            )
            seen_titles.add(title_key)
        return topics

    def _clamp_score(self, value: Any) -> float:
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            numeric = 0.0
        return max(0.0, min(100.0, numeric))

    def _title_key(self, value: str) -> str:
        return "".join(value.lower().split())
