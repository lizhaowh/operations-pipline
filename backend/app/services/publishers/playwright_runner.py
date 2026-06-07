from dataclasses import dataclass

from app.core.config import get_settings


@dataclass
class PlaywrightRunbook:
    platform: str
    launch_mode: str
    storage_state_path: str | None
    start_url: str | None
    selectors: dict[str, str]
    steps: list[str]
    notes: list[str]


class PlaywrightRunner:
    def __init__(self) -> None:
        self.settings = get_settings()

    def build_runbook(self, *, platform: str) -> PlaywrightRunbook:
        if platform == "xiaohongshu":
            return self._build_xiaohongshu_runbook()
        return self._build_generic_runbook(platform)

    def _build_xiaohongshu_runbook(self) -> PlaywrightRunbook:
        return PlaywrightRunbook(
            platform="xiaohongshu",
            launch_mode="connect_existing_session",
            storage_state_path=self.settings.playwright_storage_state_path,
            start_url=self.settings.xiaohongshu_creator_url,
            selectors={
                "title_input": "input[placeholder*='标题']",
                "editor_root": ".ql-editor",
                "tag_input": "input[placeholder*='标签']",
                "cover_upload": "input[type='file']",
                "publish_button": "button:has-text('发布')",
            },
            steps=[
                "启动带登录态的浏览器上下文，必要时加载 storage state。",
                "进入小红书创作后台发布页并等待编辑器完成渲染。",
                "填充标题、正文、标签和封面素材，停在最终发布确认前。",
            ],
            notes=[
                "小红书页面结构经常调整，选择器需要定期校验。",
                "建议实际执行时先使用 headed 模式，避免调试成本过高。",
                "上传图片、封面裁切和发布确认通常需要保留人工确认节点。",
            ],
        )

    def _build_generic_runbook(self, platform: str) -> PlaywrightRunbook:
        return PlaywrightRunbook(
            platform=platform,
            launch_mode="connect_existing_session",
            storage_state_path=self.settings.playwright_storage_state_path,
            start_url=None,
            selectors={},
            steps=[
                "启动带登录态的浏览器上下文。",
                "进入平台创作页并等待页面稳定。",
                "按字段填充内容，停在最终发布确认前。",
            ],
            notes=[
                "当前平台尚未配置站点级选择器。",
                "需要后续补充具体页面结构和字段映射。",
            ],
        )
