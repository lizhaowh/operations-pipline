from openai import OpenAI

from app.core.config import get_settings


class LLMGateway:
    def __init__(self) -> None:
        settings = get_settings()
        self.client = OpenAI(
            base_url=settings.dashscope_base_url,
            api_key=settings.dashscope_api_key,
        )
        self.model = settings.dashscope_model

    def chat(self, messages: list[dict], temperature: float = 0.7) -> dict:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        return {
            "content": response.choices[0].message.content,
            "usage": getattr(response, "usage", None),
        }

