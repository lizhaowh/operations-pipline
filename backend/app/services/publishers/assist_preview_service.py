from app.services.publishers.xiaohongshu_executor import XiaohongshuPlaywrightExecutor


class AssistedPublishPreviewService:
    def build_preview(self, *, asset):
        if asset.platform == "xiaohongshu":
            return XiaohongshuPlaywrightExecutor().build_preview(asset=asset)
        raise ValueError(f"no assisted publish executor for platform: {asset.platform}")

    async def execute_until_publish_confirmation(self, *, asset):
        if asset.platform == "xiaohongshu":
            return await XiaohongshuPlaywrightExecutor().execute_until_publish_confirmation(asset=asset)
        raise ValueError(f"no assisted publish executor for platform: {asset.platform}")
