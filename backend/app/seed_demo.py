from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, select

from app.core.db import SessionLocal
from app.models.brand_profile import BrandProfile
from app.models.content_asset import ContentAsset
from app.models.content_task import ContentTask
from app.models.media_asset import MediaAsset
from app.models.project import Project
from app.models.publish_job import PublishJob
from app.models.publish_result import PublishResult
from app.models.topic_candidate import TopicCandidate

DEMO_PROJECT_NAME = "Demo Content Automation"


def seed_demo() -> None:
    with SessionLocal() as db:
        existing = db.scalar(select(Project).where(Project.name == DEMO_PROJECT_NAME))
        if existing is not None:
            db.execute(delete(Project).where(Project.id == existing.id))
            db.commit()

        project = Project(
            name=DEMO_PROJECT_NAME,
            industry="AI SaaS",
            goal="演示从品牌配置到选题、内容、审核、发布的完整闭环",
            status="active",
        )
        db.add(project)
        db.commit()
        db.refresh(project)

        brand_profile = BrandProfile(
            project_id=project.id,
            brand_name="Orbit Content Lab",
            brand_desc="帮助中小团队把内容生产流程做成可复用系统。",
            target_audience="创业团队负责人、内容运营负责人、个人 IP",
            tone_of_voice="专业、直接、可执行",
            product_info_json={"offer": "内容自动化增长系统", "delivery": "SaaS + 服务"},
            cta_rules_json={"cta": "领取内容自动化方案模板"},
            banned_words_json=["包过", "稳赚", "绝对"],
            competitor_accounts_json=[
                {"platform": "xiaohongshu", "name": "AIGC 增长研究所"},
                {"platform": "wechat", "name": "内容增长笔记"},
            ],
            extra_context="重点展示企业服务场景，不做夸张营销表达。",
        )
        db.add(brand_profile)
        db.commit()

        topics = [
            TopicCandidate(
                project_id=project.id,
                title="为什么多数团队做内容却拿不到稳定线索",
                angle="从选题、结构和复盘机制三层拆解内容失效原因",
                source_type="seed_demo",
                source_payload_json={"demo": True},
                heat_score=74,
                relevance_score=88,
                conversion_score=86,
                competition_score=43,
                final_score=77.1,
                reason="适合企业服务类品牌做高转化内容演示",
                status="approved",
            ),
            TopicCandidate(
                project_id=project.id,
                title="内容自动化系统第一版应该怎么搭",
                angle="按工作流而不是按单个 prompt 组织系统能力",
                source_type="seed_demo",
                source_payload_json={"demo": True},
                heat_score=79,
                relevance_score=92,
                conversion_score=81,
                competition_score=39,
                final_score=81.8,
                reason="适合作为产品方案类内容示例",
                status="in_production",
            ),
            TopicCandidate(
                project_id=project.id,
                title="小团队如何把公众号和小红书共用一套内容资产",
                angle="围绕多平台复用和差异化改写给出执行模板",
                source_type="seed_demo",
                source_payload_json={"demo": True},
                heat_score=71,
                relevance_score=90,
                conversion_score=78,
                competition_score=35,
                final_score=79.1,
                reason="适合展示多平台改写和发布能力",
                status="new",
            ),
        ]
        db.add_all(topics)
        db.commit()
        for topic in topics:
            db.refresh(topic)

        now = datetime.now(timezone.utc)
        task = ContentTask(
            project_id=project.id,
            topic_id=topics[1].id,
            workflow_type="article_generation",
            status="pending_review",
            created_at=now - timedelta(hours=6),
            updated_at=now - timedelta(hours=1),
        )
        db.add(task)
        db.commit()
        db.refresh(task)

        wechat_asset = ContentAsset(
            task_id=task.id,
            platform="wechat",
            asset_type="article",
            title="内容自动化系统第一版应该怎么搭",
            outline_json={
                "sections": [
                    {"heading": "问题背景", "points": ["为什么团队会被内容生产卡住", "单点工具的局限"]},
                    {"heading": "系统设计", "points": ["工作流优先", "审核节点", "发布与复盘"]},
                    {"heading": "落地建议", "points": ["先做 MVP", "先做两个平台", "保留人工审核"]},
                ]
            },
            content_markdown=(
                "# 内容自动化系统第一版应该怎么搭\n\n"
                "很多团队把内容生产理解成写稿工具，但真正需要的是一条完整工作流。\n\n"
                "第一版应该优先把品牌配置、选题池、内容生成、审核和发布串起来。"
            ),
            summary="公众号长文版本，适合讲清楚系统设计逻辑。",
            tags_json=["内容系统", "公众号运营", "AIGC"],
            cover_text="内容自动化第一版",
            cta_text="回复“自动化”领取系统设计清单",
            review_status="approved",
            created_at=now - timedelta(hours=5),
            updated_at=now - timedelta(hours=2),
        )
        xhs_asset = ContentAsset(
            task_id=task.id,
            platform="xiaohongshu",
            asset_type="article",
            title="内容自动化系统第一版应该怎么搭",
            outline_json={
                "sections": [
                    {"heading": "先说结论", "points": ["不要一上来就做全自动", "先把闭环跑通"]},
                    {"heading": "怎么搭", "points": ["品牌配置", "选题池", "内容工作台"]},
                    {"heading": "怎么发", "points": ["人工审核", "辅助发布", "数据回收"]},
                ]
            },
            content_markdown=(
                "# 内容自动化系统第一版应该怎么搭\n\n"
                "别一上来就想着无人值守。\n\n"
                "第一版最重要的是把选题、写作、审核、发布和复盘做成固定流程。"
            ),
            summary="小红书图文版本，强调执行路径和避坑。",
            tags_json=["内容自动化", "小红书运营", "AIGC"],
            cover_text="先闭环再自动化",
            cta_text="私信我“模板”拿流程图",
            review_status="approved",
            created_at=now - timedelta(hours=5),
            updated_at=now - timedelta(hours=2),
        )
        db.add_all([wechat_asset, xhs_asset])
        db.commit()
        db.refresh(wechat_asset)
        db.refresh(xhs_asset)

        media_assets = [
            MediaAsset(
                task_id=task.id,
                content_asset_id=wechat_asset.id,
                platform="wechat",
                media_type="image",
                role="cover",
                title="公众号封面图",
                prompt_text="蓝色企业服务风格，突出内容自动化第一版方法论，适合公众号头图。",
                file_url="data:image/svg+xml;charset=UTF-8,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20width%3D%221200%22%20height%3D%22630%22%20viewBox%3D%220%200%201200%20630%22%3E%3Crect%20width%3D%221200%22%20height%3D%22630%22%20fill%3D%22%230f172a%22/%3E%3Crect%20x%3D%2248%22%20y%3D%2248%22%20width%3D%221104%22%20height%3D%22534%22%20rx%3D%2228%22%20fill%3D%22%231677ff%22%20fill-opacity%3D%220.18%22/%3E%3Ctext%20x%3D%2272%22%20y%3D%22130%22%20fill%3D%22%23cbd5e1%22%20font-size%3D%2230%22%20font-family%3D%22Arial%22%3EContent%20Orbit%20Demo%3C/text%3E%3Ctext%20x%3D%2272%22%20y%3D%22280%22%20fill%3D%22white%22%20font-size%3D%2258%22%20font-family%3D%22Arial%22%20font-weight%3D%22700%22%3E内容自动化第一版怎么搭%3C/text%3E%3Ctext%20x%3D%2272%22%20y%3D%22356%22%20fill%3D%22%23e2e8f0%22%20font-size%3D%2230%22%20font-family%3D%22Arial%22%3E公众号封面演示图%3C/text%3E%3C/svg%3E",
                status="generated",
                metadata_json={"width": 1200, "height": 630},
            ),
            MediaAsset(
                task_id=task.id,
                content_asset_id=xhs_asset.id,
                platform="xiaohongshu",
                media_type="image",
                role="cover",
                title="小红书首图",
                prompt_text="红色高对比封面，突出先闭环再自动化，适合小红书图文首图。",
                file_url="data:image/svg+xml;charset=UTF-8,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20width%3D%221200%22%20height%3D%22630%22%20viewBox%3D%220%200%201200%20630%22%3E%3Crect%20width%3D%221200%22%20height%3D%22630%22%20fill%3D%22%230f172a%22/%3E%3Crect%20x%3D%2248%22%20y%3D%2248%22%20width%3D%221104%22%20height%3D%22534%22%20rx%3D%2228%22%20fill%3D%22%23ef4444%22%20fill-opacity%3D%220.18%22/%3E%3Ctext%20x%3D%2272%22%20y%3D%22130%22%20fill%3D%22%23fecaca%22%20font-size%3D%2230%22%20font-family%3D%22Arial%22%3EContent%20Orbit%20Demo%3C/text%3E%3Ctext%20x%3D%2272%22%20y%3D%22280%22%20fill%3D%22white%22%20font-size%3D%2258%22%20font-family%3D%22Arial%22%20font-weight%3D%22700%22%3E先闭环 再自动化%3C/text%3E%3Ctext%20x%3D%2272%22%20y%3D%22356%22%20fill%3D%22%23fee2e2%22%20font-size%3D%2230%22%20font-family%3D%22Arial%22%3E小红书首图演示%3C/text%3E%3C/svg%3E",
                status="generated",
                metadata_json={"width": 1200, "height": 630},
            ),
        ]
        db.add_all(media_assets)
        db.commit()

        manual_job = PublishJob(
            task_id=task.id,
            content_asset_id=wechat_asset.id,
            platform="wechat",
            publish_mode="manual_export",
            status="success",
            started_at=now - timedelta(hours=1),
            finished_at=now - timedelta(minutes=50),
        )
        assisted_job = PublishJob(
            task_id=task.id,
            content_asset_id=xhs_asset.id,
            platform="xiaohongshu",
            publish_mode="assisted_publish",
            status="draft",
        )
        db.add_all([manual_job, assisted_job])
        db.commit()
        db.refresh(manual_job)
        db.refresh(assisted_job)

        publish_result = PublishResult(
            publish_job_id=manual_job.id,
            platform_post_id="demo-wechat-001",
            post_url="https://example.com/demo/wechat-001",
            published_at=now - timedelta(minutes=50),
            raw_response_json={
                "mode": "manual_export",
                "platform": "wechat",
                "export_package": {
                    "title": wechat_asset.title,
                    "summary": wechat_asset.summary,
                    "tags": wechat_asset.tags_json,
                },
                "next_steps": [
                    "复制正文到公众号草稿箱",
                    "上传配图并检查排版",
                    "发布后回填真实链接",
                ],
            },
        )
        db.add(publish_result)
        db.commit()

        print("Demo data seeded successfully.")
        print(f"Project: {project.name}")
        print(f"Project ID: {project.id}")
        print(f"Content Task ID: {task.id}")
        print(f"WeChat Asset ID: {wechat_asset.id}")
        print(f"Xiaohongshu Asset ID: {xhs_asset.id}")


if __name__ == "__main__":
    seed_demo()
