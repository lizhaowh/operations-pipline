import json
from time import perf_counter

from app.core.config import get_settings
from app.services.llm.gateway import LLMGateway
from app.services.repositories.llm_log_repo import LLMLogRepository


class ContentLLMService:
    def __init__(self, llm_log_repo: LLMLogRepository):
        self.settings = get_settings()
        self.gateway = LLMGateway()
        self.llm_log_repo = llm_log_repo

    def generate_article_bundle(
        self,
        *,
        project_id: int,
        topic_title: str,
        topic_angle: str | None,
        platform: str,
    ) -> dict:
        if not self.settings.dashscope_api_key:
            return self._fallback_bundle(topic_title=topic_title, topic_angle=topic_angle, platform=platform)

        system_prompt = (
            "你是一个内容策略编辑。"
            "请输出严格 JSON，字段包括 title, summary, cover_text, cta_text, tags_json, outline_json, content_markdown。"
            "不要输出 markdown 代码块。"
        )
        user_prompt = (
            f"平台：{platform}\n"
            f"选题：{topic_title}\n"
            f"角度：{topic_angle or '围绕用户痛点给出可执行建议'}\n"
            "要求：适配对应平台语气，给出清晰结构、可执行建议和简短 CTA。"
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        started = perf_counter()
        try:
            result = self.gateway.chat(messages, temperature=0.7)
            latency_ms = int((perf_counter() - started) * 1000)
            content = result["content"] or "{}"
            parsed = json.loads(content)
            usage = result.get("usage")
            self.llm_log_repo.create(
                project_id=project_id,
                scene="article_bundle_generation",
                model=self.gateway.model,
                request_payload_json={"messages": messages, "platform": platform},
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
                scene="article_bundle_generation",
                model=self.gateway.model,
                request_payload_json={"messages": messages, "platform": platform},
                response_text=None,
                prompt_tokens=None,
                completion_tokens=None,
                latency_ms=latency_ms,
                status="failed",
                error_message=str(exc),
            )
            return self._fallback_bundle(topic_title=topic_title, topic_angle=topic_angle, platform=platform)

    def _fallback_bundle(self, *, topic_title: str, topic_angle: str | None, platform: str) -> dict:
        angle = topic_angle or "围绕用户痛点给出可执行建议"
        if platform == "xiaohongshu":
            tags = ["内容运营", "内容自动化", "选题", "小红书运营"]
            content = (
                f"# {topic_title}\n\n"
                "做内容最怕的不是没灵感，而是方向反复摇摆。\n\n"
                f"这篇先讲清楚一个核心角度：{angle}。\n\n"
                "1. 为什么这个问题会反复出现。\n"
                "2. 应该如何拆解成可执行步骤。\n"
                "3. 哪些动作适合今天就开始做。"
            )
        else:
            tags = ["内容系统", "公众号运营", "内容增长"]
            content = (
                f"# {topic_title}\n\n"
                f"本文围绕“{angle}”展开，目的是把抽象问题拆成实际可落地的内容动作。\n\n"
                "## 一、问题背景\n\n"
                "很多团队并不是不会写，而是没有固定的内容生产系统。\n\n"
                "## 二、拆解方法\n\n"
                "把选题、结构、改写、发布和复盘做成标准流程。\n\n"
                "## 三、落地建议\n\n"
                "优先固定输入来源、内容模板和审核机制。"
            )
        return {
            "title": topic_title,
            "summary": f"围绕《{topic_title}》输出适合 {platform} 的结构化内容草稿。",
            "cover_text": topic_title[:32],
            "cta_text": "如果你希望持续稳定产出内容，可以把选题、写作和复盘做成固定流程。",
            "tags_json": tags,
            "outline_json": {
                "platform": platform,
                "sections": [
                    {"heading": "问题背景", "points": [f"为什么要讨论《{topic_title}》", angle]},
                    {"heading": "核心拆解", "points": ["常见错误", "底层原因", "可执行方法"]},
                    {"heading": "行动建议", "points": ["适用场景", "落地步骤", "下一步 CTA"]},
                ],
            },
            "content_markdown": content,
        }

