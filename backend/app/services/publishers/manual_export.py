from app.services.publishers.base import BasePublisher, PublishPayload


class ManualExportPublisher(BasePublisher):
    mode = "manual_export"

    def build_payload(self, asset) -> PublishPayload:
        raw = {
            "mode": self.mode,
            "platform": asset.platform,
            "platform_post_id": f"export-{asset.platform}-{asset.id}",
            "post_url": None,
            "export_package": {
                "title": asset.title,
                "summary": asset.summary,
                "cover_text": asset.cover_text,
                "tags": asset.tags_json or [],
                "content_markdown": asset.content_markdown,
                "cta_text": asset.cta_text,
            },
            "next_steps": [
                "复制导出包中的标题、正文、标签和封面文案。",
                "在目标平台新建内容并手动粘贴。",
                "发布后把真实链接回填到系统中。",
            ],
        }
        return PublishPayload(
            mode=self.mode,
            platform_post_id=raw["platform_post_id"],
            post_url=raw["post_url"],
            raw_response_json=raw,
        )

