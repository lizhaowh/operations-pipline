from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from app.core.config import get_settings
from app.services.publishers.playwright_runner import PlaywrightRunner


@dataclass
class ExecutionCheck:
    ok: bool
    code: str
    message: str


@dataclass
class ExecutionPreview:
    platform: str
    can_run: bool
    launch_mode: str
    start_url: str | None
    storage_state_path: str | None
    selectors: dict[str, str]
    checks: list[ExecutionCheck]
    steps: list[str]
    notes: list[str]
    payload_summary: dict[str, Any]


class XiaohongshuPlaywrightExecutor:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.runner = PlaywrightRunner()

    def build_preview(self, *, asset) -> ExecutionPreview:
        runbook = self.runner.build_runbook(platform="xiaohongshu")
        checks = self._validate_environment(runbook.storage_state_path)
        can_run = all(item.ok for item in checks)
        payload_summary = {
            "title": asset.title,
            "summary": asset.summary,
            "cover_text": asset.cover_text,
            "tags": asset.tags_json or [],
            "content_length": len(asset.content_markdown or ""),
        }
        return ExecutionPreview(
            platform="xiaohongshu",
            can_run=can_run,
            launch_mode=runbook.launch_mode,
            start_url=runbook.start_url,
            storage_state_path=runbook.storage_state_path,
            selectors=runbook.selectors,
            checks=checks,
            steps=runbook.steps,
            notes=runbook.notes,
            payload_summary=payload_summary,
        )

    async def execute_until_publish_confirmation(self, *, asset) -> dict[str, Any]:
        """
        Skeleton only:
        1. launch browser/context with existing login state
        2. open creator page
        3. fill title/body/tags
        4. stop before final publish confirmation
        """
        preview = self.build_preview(asset=asset)
        if not preview.can_run:
            return {
                "status": "blocked",
                "reason": "environment_not_ready",
                "checks": [asdict(item) for item in preview.checks],
            }

        from playwright.async_api import async_playwright

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=self.settings.playwright_headless,
                channel=self.settings.playwright_browser_channel or None,
            )
            context_kwargs: dict[str, Any] = {}
            if preview.storage_state_path:
                context_kwargs["storage_state"] = preview.storage_state_path
            context = await browser.new_context(**context_kwargs)
            page = await context.new_page()
            if preview.start_url:
                await page.goto(preview.start_url, wait_until="domcontentloaded")

            selectors = preview.selectors
            if selectors.get("title_input") and asset.title:
                await page.locator(selectors["title_input"]).fill(asset.title)

            if selectors.get("editor_root") and asset.content_markdown:
                await page.locator(selectors["editor_root"]).fill(asset.content_markdown)

            if selectors.get("tag_input") and asset.tags_json:
                for tag in asset.tags_json:
                    await page.locator(selectors["tag_input"]).fill(tag)
                    await page.locator(selectors["tag_input"]).press("Enter")

            return {
                "status": "ready_for_manual_confirmation",
                "platform": "xiaohongshu",
                "start_url": preview.start_url,
                "filled_fields": {
                    "title": bool(asset.title),
                    "content_markdown": bool(asset.content_markdown),
                    "tags": len(asset.tags_json or []),
                },
                "next_action": "operator_confirms_before_clicking_publish",
            }

    def _validate_environment(self, storage_state_path: str | None) -> list[ExecutionCheck]:
        checks: list[ExecutionCheck] = []
        checks.append(
            ExecutionCheck(
                ok=bool(self.settings.xiaohongshu_creator_url),
                code="creator_url",
                message="xiaohongshu creator url configured" if self.settings.xiaohongshu_creator_url else "missing xiaohongshu creator url",
            )
        )

        if storage_state_path:
            exists = Path(storage_state_path).exists()
            checks.append(
                ExecutionCheck(
                    ok=exists,
                    code="storage_state",
                    message=f"storage state found: {storage_state_path}" if exists else f"storage state missing: {storage_state_path}",
                )
            )
        else:
            checks.append(
                ExecutionCheck(
                    ok=False,
                    code="storage_state",
                    message="missing PLAYWRIGHT_STORAGE_STATE_PATH for logged-in browser context",
                )
            )

        checks.append(
            ExecutionCheck(
                ok=True,
                code="publisher_mode",
                message="executor skeleton is available; actual publish confirmation still requires operator review",
            )
        )
        return checks

