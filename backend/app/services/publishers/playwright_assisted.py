from app.services.publishers.base import BasePublisher, PublishPayload
from app.services.publishers.playwright_runner import PlaywrightRunner


class PlaywrightAssistedPublisher(BasePublisher):
    mode = "assisted_publish"

    def __init__(self) -> None:
        self.runner = PlaywrightRunner()

    def build_payload(self, asset) -> PublishPayload:
        runbook = self.runner.build_runbook(platform=asset.platform)
        raw = {
            "mode": self.mode,
            "platform": asset.platform,
            "platform_post_id": f"assist-{asset.platform}-{asset.id}",
            "post_url": None,
            "automation": {
                "engine": "playwright",
                "status": "scaffold_ready",
                "launch_mode": runbook.launch_mode,
                "storage_state_path": runbook.storage_state_path,
                "start_url": runbook.start_url,
                "selectors": runbook.selectors,
                "required_steps": runbook.steps,
                "notes": runbook.notes,
            },
            "assistant_steps": runbook.steps,
            "form_payload": {
                "title": asset.title,
                "summary": asset.summary,
                "cover_text": asset.cover_text,
                "tags": asset.tags_json or [],
                "content_markdown": asset.content_markdown,
                "cta_text": asset.cta_text,
            },
        }
        return PublishPayload(
            mode=self.mode,
            platform_post_id=raw["platform_post_id"],
            post_url=raw["post_url"],
            raw_response_json=raw,
        )
