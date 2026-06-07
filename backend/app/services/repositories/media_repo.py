from urllib.parse import quote

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.content_asset import ContentAsset
from app.models.content_task import ContentTask
from app.models.media_asset import MediaAsset


def build_demo_svg_data_url(title: str, subtitle: str, accent: str) -> str:
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
      <defs>
        <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#0f172a"/>
          <stop offset="100%" stop-color="{accent}"/>
        </linearGradient>
      </defs>
      <rect width="1200" height="630" fill="url(#g)"/>
      <rect x="48" y="48" width="1104" height="534" rx="28" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.18)"/>
      <text x="72" y="116" fill="#cbd5e1" font-size="28" font-family="Arial, PingFang SC, Microsoft YaHei">Content Orbit Demo</text>
      <text x="72" y="250" fill="#ffffff" font-size="56" font-weight="700" font-family="Arial, PingFang SC, Microsoft YaHei">{title}</text>
      <text x="72" y="330" fill="#e2e8f0" font-size="30" font-family="Arial, PingFang SC, Microsoft YaHei">{subtitle}</text>
      <text x="72" y="556" fill="#bfdbfe" font-size="24" font-family="Arial, PingFang SC, Microsoft YaHei">素材中心演示图，仅用于后台预览</text>
    </svg>
    """.strip()
    return f"data:image/svg+xml;charset=UTF-8,{quote(svg)}"


class MediaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_content_asset_or_404(self, content_asset_id: int) -> ContentAsset:
        item = self.db.get(ContentAsset, content_asset_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="content asset not found")
        return item

    def list_by_project(self, project_id: int) -> list[MediaAsset]:
        stmt = (
            select(MediaAsset)
            .join(ContentTask, ContentTask.id == MediaAsset.task_id)
            .where(ContentTask.project_id == project_id)
            .order_by(MediaAsset.id.desc())
        )
        return list(self.db.scalars(stmt))

    def list_by_task(self, task_id: int) -> list[MediaAsset]:
        stmt = select(MediaAsset).where(MediaAsset.task_id == task_id).order_by(MediaAsset.id.asc())
        return list(self.db.scalars(stmt))

    def list_by_content_asset(self, content_asset_id: int) -> list[MediaAsset]:
        stmt = (
            select(MediaAsset)
            .where(MediaAsset.content_asset_id == content_asset_id)
            .order_by(MediaAsset.id.asc())
        )
        return list(self.db.scalars(stmt))

    def create_media_asset(
        self,
        *,
        task_id: int,
        content_asset_id: int | None,
        platform: str,
        role: str,
        title: str,
        prompt_text: str,
        file_url: str,
        metadata_json: dict[str, object],
    ) -> MediaAsset:
        item = MediaAsset(
            task_id=task_id,
            content_asset_id=content_asset_id,
            platform=platform,
            media_type="image",
            role=role,
            title=title,
            prompt_text=prompt_text,
            file_url=file_url,
            status="generated",
            metadata_json=metadata_json,
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def create_demo_media_for_asset(self, content_asset_id: int, roles: list[str]) -> list[MediaAsset]:
        asset = self.get_content_asset_or_404(content_asset_id)
        existing = self.list_by_content_asset(content_asset_id)
        if existing:
          return existing

        accent = "#1677ff" if asset.platform == "wechat" else "#ef4444"
        created: list[MediaAsset] = []
        normalized_roles = roles or ["cover", "body"]

        for index, role in enumerate(normalized_roles, start=1):
            role_title = "封面图" if role == "cover" else f"配图 {index - 1}"
            title = f"{asset.title or asset.platform} - {role_title}"
            subtitle = asset.cover_text or asset.summary or "自动生成的演示素材"
            prompt_text = (
                f"为 {asset.platform} 平台生成 {role_title}。"
                f"标题：{asset.title or '未命名内容'}。"
                f"摘要：{asset.summary or '无摘要'}。"
                f"风格：专业、干净、适合中国内容运营后台演示。"
            )
            file_url = build_demo_svg_data_url(title, subtitle[:36], accent)
            metadata_json = {
                "source_platform": asset.platform,
                "source_asset_id": asset.id,
                "width": 1200,
                "height": 630,
            }
            created.append(
                MediaAsset(
                    task_id=asset.task_id,
                    content_asset_id=asset.id,
                    platform=asset.platform,
                    media_type="image",
                    role=role,
                    title=title,
                    prompt_text=prompt_text,
                    file_url=file_url,
                    status="generated",
                    metadata_json=metadata_json,
                )
            )

        self.db.add_all(created)
        self.db.commit()
        for item in created:
            self.db.refresh(item)
        return created
