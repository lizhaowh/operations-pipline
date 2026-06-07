# 自动化内容生产产品方案

## 1. 第一版 PRD

### 1.1 产品目标

做一个面向中小团队/个人 IP 的内容自动化系统，完成：

- 选题发现
- 内容生成
- 多平台改写
- 人工审核
- 发布记录
- 数据复盘

第一版目标不是“全自动爆文”，而是：

- 提升内容产能
- 降低选题和写作成本
- 建立可持续优化的内容闭环

### 1.2 目标用户

第一版用户画像：

- 个人 IP
- 小型内容团队
- 创业公司市场团队
- 代运营团队

他们的典型痛点：

- 不知道每天写什么
- 写得慢
- 不同平台要重复改写
- 发布和复盘分散
- 内容数据难沉淀成策略

### 1.3 MVP 范围

第一版只支持：

- 平台：`公众号`、`小红书`
- 内容类型：`图文长文`、`平台改写稿`
- 发布模式：`人工审核后发布`
- 分析周期：`24h / 72h / 7d`

第一版不做：

- 短视频自动剪辑
- 多租户复杂权限
- 十个平台接入
- 自由聊天式 agent
- 全自动无人审核发布

### 1.4 用户核心流程

完整流程：

1. 创建项目
2. 配置品牌信息
3. 系统生成选题池
4. 用户挑选选题进入生产
5. 系统生成大纲、正文、平台改写稿
6. 用户审核并修改
7. 定时发布或记录手动发布
8. 系统抓取表现数据
9. 系统输出复盘建议

### 1.5 页面设计

#### 1.5.1 Dashboard

目的：给用户看到当前内容生产状态。

模块：

- 今日待处理选题数
- 待审核草稿数
- 待发布内容数
- 最近 7 天数据趋势
- 本周最佳内容
- 最近失败任务告警

主要操作：

- 进入选题池
- 进入待审核内容
- 进入发布中心
- 查看周报

#### 1.5.2 项目与品牌配置页

字段：

- 项目名称
- 行业赛道
- 目标用户
- 品牌介绍
- 核心产品/服务
- 内容语气风格
- 禁用词
- 竞品账号
- 平台账号配置
- CTA 模板

操作：

- 保存品牌画像
- 更新平台配置
- 测试模型连通性

#### 1.5.3 选题池

列表字段：

- 选题标题
- 角度
- 来源
- 热度分
- 相关性分
- 转化分
- 综合分
- 推荐平台
- 状态

状态：

- `new`
- `approved`
- `discarded`
- `in_production`

操作：

- 批量生成选题
- 查看推荐理由
- 批准进入生产
- 废弃
- 手动新增选题

#### 1.5.4 内容工作台

这是第一版核心页面。

页面区域：

- 左侧：选题信息
- 中间：大纲/正文/改写内容
- 右侧：标题、摘要、标签、审核结果

生成流程：

- 生成大纲
- 生成全文
- 生成公众号版
- 生成小红书版
- 生成标题候选
- 生成标签和 CTA

操作：

- 重新生成某一段
- 一键改写成另一平台风格
- 保存版本
- 提交审核
- 审核通过后进入发布

#### 1.5.5 审核与发布中心

列表字段：

- 内容标题
- 平台
- 审核状态
- 发布时间
- 发布状态
- 错误信息

审核状态：

- `pending_review`
- `approved`
- `rejected`

发布状态：

- `draft`
- `scheduled`
- `publishing`
- `published`
- `failed`

操作：

- 通过审核
- 驳回并填写原因
- 设置发布时间
- 立即发布
- 失败重试
- 查看发布链接

#### 1.5.6 数据分析页

模块：

- 总发布数
- 平均阅读/互动
- 平台对比
- 选题类型表现
- 标题风格表现
- 发布时间表现
- 周报建议

操作：

- 按项目/平台/时间筛选
- 查看单篇内容表现
- 生成周报
- 导出分析结果

### 1.6 状态流转设计

选题状态：

- `new`
- `approved`
- `discarded`
- `in_production`

内容任务状态：

- `draft_requested`
- `outline_generated`
- `article_generated`
- `rewritten`
- `pending_review`
- `approved`
- `rejected`
- `publish_pending`
- `published`
- `analyzed`

发布任务状态：

- `scheduled`
- `running`
- `success`
- `failed`

### 1.7 系统自动化规则

每日任务建议：

- `08:00` 抓热点/竞品内容
- `08:10` 生成选题池
- `08:30` 为高分选题生成建议
- `每小时` 执行到期发布任务
- `发布后 24h/72h/7d` 抓取数据
- `每周一 09:00` 生成周报

### 1.8 验收标准

MVP 上线前，最少满足：

- 能创建项目和品牌资料
- 能生成 10 个以上候选选题
- 能针对选题生成长文和平台改写稿
- 能人工审核和定时发布
- 能记录发布状态
- 能看到基础数据统计和周报建议

## 2. 后端工程脚手架设计

### 2.1 技术栈

建议：

- `FastAPI`
- `PostgreSQL`
- `Redis`
- `Celery`
- `SQLAlchemy 2.0`
- `Alembic`
- `Pydantic v2`
- `Playwright`
- `openai` SDK 兼容阿里百炼接口

### 2.2 目录结构

```text
backend/
  app/
    api/
      v1/
        router.py
        endpoints/
          projects.py
          brand_profiles.py
          topics.py
          contents.py
          publish.py
          analytics.py
          workflows.py
    core/
      config.py
      db.py
      redis.py
      logger.py
      security.py
    models/
      project.py
      brand_profile.py
      platform_account.py
      topic_candidate.py
      content_task.py
      content_asset.py
      publish_job.py
      publish_result.py
      content_metric.py
      workflow_run.py
      llm_call_log.py
    schemas/
      project.py
      brand_profile.py
      topic.py
      content.py
      publish.py
      analytics.py
      common.py
    services/
      llm/
        gateway.py
        prompts.py
        parser.py
      agents/
        topic_agent.py
        writer_agent.py
        reviewer_agent.py
        analytics_agent.py
      tools/
        hot_topics.py
        competitor_fetcher.py
        deduplicator.py
        publisher/
          base.py
          wechat.py
          xiaohongshu.py
        metrics/
          wechat.py
          xiaohongshu.py
      workflows/
        topic_workflow.py
        content_workflow.py
        publish_workflow.py
        analytics_workflow.py
      repositories/
        project_repo.py
        topic_repo.py
        content_repo.py
        publish_repo.py
        analytics_repo.py
    tasks/
      celery_app.py
      topic_tasks.py
      content_tasks.py
      publish_tasks.py
      analytics_tasks.py
      beat_schedule.py
    utils/
      enums.py
      time.py
      json_utils.py
    main.py
  alembic/
  tests/
  .env.example
  pyproject.toml
  Dockerfile
  docker-compose.yml
```

### 2.3 核心模块职责

`api`

- 只处理 HTTP 请求和响应
- 不写复杂业务逻辑

`services/agents`

- 封装“业务智能体”
- 每个 agent 输入输出固定

`services/workflows`

- 串联多步骤任务
- 做状态推进和异常处理

`services/tools`

- 封装外部能力
- 例如抓取、发布、指标采集

`tasks`

- 异步执行
- 重试
- 定时调度

`repositories`

- 数据访问
- 避免 service 里到处写 SQLAlchemy

### 2.4 配置文件设计

`.env.example`

```env
APP_ENV=dev
APP_HOST=0.0.0.0
APP_PORT=8000

DATABASE_URL=postgresql+psycopg://postgres:postgres@139.224.189.13:5432/auto_content
REDIS_URL=redis://localhost:6379/0

DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
DASHSCOPE_API_KEY=replace_me
DASHSCOPE_MODEL=qwen-plus

CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
```

### 2.5 FastAPI 模块组织

总路由：

```python
/api/v1/projects
/api/v1/brand-profiles
/api/v1/topics
/api/v1/contents
/api/v1/publish
/api/v1/analytics
/api/v1/workflows
```

`router.py`

```python
from fastapi import APIRouter
from app.api.v1.endpoints import projects, topics, contents, publish, analytics

api_router = APIRouter()
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(topics.router, prefix="/topics", tags=["topics"])
api_router.include_router(contents.router, prefix="/contents", tags=["contents"])
api_router.include_router(publish.router, prefix="/publish", tags=["publish"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
```

### 2.6 Agent 代码组织方式

`topic_agent.py`

```python
class TopicAgent:
    async def generate_candidates(self, project_id: int) -> list[dict]:
        ...
```

`writer_agent.py`

```python
class WriterAgent:
    async def generate_outline(self, topic_id: int) -> dict:
        ...

    async def generate_article(self, topic_id: int) -> dict:
        ...

    async def rewrite_for_platform(self, asset_id: int, platform: str) -> dict:
        ...
```

`reviewer_agent.py`

```python
class ReviewerAgent:
    async def review_asset(self, asset_id: int) -> dict:
        ...
```

`analytics_agent.py`

```python
class AnalyticsAgent:
    async def generate_weekly_report(self, project_id: int) -> dict:
        ...
```

原则：

- 返回结构化数据
- 每一步单一职责
- 每一步可重试

### 2.7 Workflow 设计

`topic_workflow.py`

- 收集热点
- 收集竞品内容
- 去重
- 调用 TopicAgent
- 入库选题

`content_workflow.py`

- 选题转内容任务
- 生成大纲
- 生成正文
- 生成平台改写稿
- 提交审核

`publish_workflow.py`

- 校验审核状态
- 调用平台 publisher
- 记录发布结果
- 安排数据采集任务

`analytics_workflow.py`

- 汇总内容指标
- 调用 AnalyticsAgent 输出建议
- 保存周报

### 2.8 异步任务设计

Celery task：

```python
generate_daily_topics(project_id)
generate_content(task_id)
review_content(asset_id)
publish_content(job_id)
collect_metrics(publish_result_id)
generate_weekly_report(project_id)
```

要求：

- 幂等
- 默认重试 3 次
- 落库任务状态
- 写 error log

### 2.9 数据模型最小集

第一版至少这些表：

- `projects`
- `brand_profiles`
- `platform_accounts`
- `topic_candidates`
- `content_tasks`
- `content_assets`
- `publish_jobs`
- `publish_results`
- `content_metrics`
- `llm_call_logs`
- `workflow_runs`

### 2.10 阿里百炼接入层

`gateway.py`

```python
from openai import OpenAI

class LLMGateway:
    def __init__(self, base_url: str, api_key: str, model: str):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model

    def chat(self, messages: list[dict], temperature: float = 0.7) -> dict:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        return {
            "content": resp.choices[0].message.content,
            "usage": getattr(resp, "usage", None),
        }
```

上层不要直接散用，统一从 scene service 调：

- `generate_topics`
- `generate_outline`
- `generate_article`
- `rewrite_platform`
- `review_content`

### 2.11 Prompt 管理方式

第一版建议先：

- 模板文件放代码里
- 模板版本记录在数据库
- 后面再升级成后台可编辑

目录：

```text
app/services/llm/prompts/
  topic_generation.txt
  outline_generation.txt
  article_generation.txt
  platform_rewrite_wechat.txt
  platform_rewrite_xiaohongshu.txt
  content_review.txt
```

### 2.12 发布适配器接口

```python
class BasePublisher:
    async def publish(self, asset: dict, account: dict) -> dict:
        raise NotImplementedError
```

实现：

- `WeChatPublisher`
- `XiaohongshuPublisher`

第一版建议支持两种模式：

- `manual_export`
- `assisted_publish`

这比一开始做纯自动发布更稳。

### 2.13 开发顺序

建议按下面顺序开工：

1. 项目骨架、配置、数据库连接
2. 项目/品牌 API
3. LLM Gateway
4. 选题工作流
5. 内容生成工作流
6. 审核状态流
7. 发布任务
8. 数据采集与分析

## 3. 可开工实现草案

### 3.1 SQLAlchemy 模型草案

以下是第一版最重要的模型骨架。

`app/models/project.py`

```python
from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    industry: Mapped[str | None] = mapped_column(String(64))
    goal: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="active", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
```

`app/models/brand_profile.py`

```python
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class BrandProfile(Base):
    __tablename__ = "brand_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    brand_name: Mapped[str] = mapped_column(String(128), nullable=False)
    brand_desc: Mapped[str | None] = mapped_column(Text)
    target_audience: Mapped[str | None] = mapped_column(Text)
    tone_of_voice: Mapped[str | None] = mapped_column(String(64))
    product_info_json: Mapped[dict | None] = mapped_column(JSONB)
    cta_rules_json: Mapped[dict | None] = mapped_column(JSONB)
    banned_words_json: Mapped[list[str] | None] = mapped_column(JSONB)
    competitor_accounts_json: Mapped[list[dict] | None] = mapped_column(JSONB)
    extra_context: Mapped[str | None] = mapped_column(Text)
```

`app/models/topic_candidate.py`

```python
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class TopicCandidate(Base):
    __tablename__ = "topic_candidates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    angle: Mapped[str | None] = mapped_column(Text)
    source_type: Mapped[str] = mapped_column(String(32), nullable=False)
    source_payload_json: Mapped[dict | None] = mapped_column(JSONB)
    heat_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    relevance_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    conversion_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    competition_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    final_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="new", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
```

`app/models/content_task.py`

```python
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class ContentTask(Base):
    __tablename__ = "content_tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topic_candidates.id", ondelete="CASCADE"), nullable=False, index=True)
    workflow_type: Mapped[str] = mapped_column(String(32), default="article_generation", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="draft_requested", nullable=False)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime)
    published_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
```

`app/models/content_asset.py`

```python
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class ContentAsset(Base):
    __tablename__ = "content_assets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("content_tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    platform: Mapped[str] = mapped_column(String(32), nullable=False)
    asset_type: Mapped[str] = mapped_column(String(32), default="article", nullable=False)
    title: Mapped[str | None] = mapped_column(String(255))
    outline_json: Mapped[dict | None] = mapped_column(JSONB)
    content_markdown: Mapped[str | None] = mapped_column(Text)
    summary: Mapped[str | None] = mapped_column(Text)
    tags_json: Mapped[list[str] | None] = mapped_column(JSONB)
    cover_text: Mapped[str | None] = mapped_column(String(255))
    cta_text: Mapped[str | None] = mapped_column(Text)
    version: Mapped[int] = mapped_column(default=1, nullable=False)
    review_status: Mapped[str] = mapped_column(String(32), default="pending_review", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
```

### 3.2 Pydantic Schema 草案

`app/schemas/project.py`

```python
from datetime import datetime

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=128)
    industry: str | None = Field(default=None, max_length=64)
    goal: str | None = None


class ProjectRead(BaseModel):
    id: int
    name: str
    industry: str | None
    goal: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
```

`app/schemas/topic.py`

```python
from datetime import datetime

from pydantic import BaseModel


class TopicRead(BaseModel):
    id: int
    project_id: int
    title: str
    angle: str | None
    source_type: str
    heat_score: float
    relevance_score: float
    conversion_score: float
    competition_score: float
    final_score: float
    reason: str | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
```

### 3.3 FastAPI 接口定义样例

`app/api/v1/endpoints/projects.py`

```python
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.project import ProjectCreate, ProjectRead
from app.services.repositories.project_repo import ProjectRepository

router = APIRouter()


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)) -> ProjectRead:
    repo = ProjectRepository(db)
    project = repo.create(payload)
    return ProjectRead.model_validate(project)


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)) -> ProjectRead:
    repo = ProjectRepository(db)
    project = repo.get_or_404(project_id)
    return ProjectRead.model_validate(project)
```

`app/api/v1/endpoints/topics.py`

```python
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.topic import TopicRead
from app.tasks.topic_tasks import generate_daily_topics
from app.services.repositories.topic_repo import TopicRepository

router = APIRouter()


@router.post("/projects/{project_id}/generate", status_code=status.HTTP_202_ACCEPTED)
def generate_topics(project_id: int) -> dict:
    generate_daily_topics.delay(project_id)
    return {"message": "topic generation queued", "project_id": project_id}


@router.get("/projects/{project_id}", response_model=list[TopicRead])
def list_topics(project_id: int, db: Session = Depends(get_db)) -> list[TopicRead]:
    repo = TopicRepository(db)
    items = repo.list_by_project(project_id)
    return [TopicRead.model_validate(item) for item in items]
```

### 3.4 Repository 设计样例

`app/services/repositories/project_repo.py`

```python
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: ProjectCreate) -> Project:
        item = Project(**payload.model_dump())
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_or_404(self, project_id: int) -> Project:
        item = self.db.get(Project, project_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project not found")
        return item
```

### 3.5 内容生成工作流伪代码

```python
class ContentWorkflowService:
    def __init__(self, writer_agent, reviewer_agent, content_repo, llm_logger):
        self.writer_agent = writer_agent
        self.reviewer_agent = reviewer_agent
        self.content_repo = content_repo
        self.llm_logger = llm_logger

    async def run(self, task_id: int) -> dict:
        task = self.content_repo.get_task_or_404(task_id)
        self.content_repo.update_task_status(task, "draft_requested")

        outline = await self.writer_agent.generate_outline(task.topic_id)
        self.content_repo.save_outline(task_id, outline)
        self.content_repo.update_task_status(task, "outline_generated")

        article = await self.writer_agent.generate_article(task.topic_id)
        self.content_repo.save_article(task_id, platform="wechat", article=article)
        self.content_repo.update_task_status(task, "article_generated")

        xiaohongshu_asset = await self.writer_agent.rewrite_for_platform(task_id, platform="xiaohongshu")
        self.content_repo.save_platform_asset(task_id, "xiaohongshu", xiaohongshu_asset)
        self.content_repo.update_task_status(task, "rewritten")

        review_result = await self.reviewer_agent.review_task_assets(task_id)
        self.content_repo.save_review_result(task_id, review_result)
        self.content_repo.update_task_status(task, "pending_review")

        return {"task_id": task_id, "status": "pending_review"}
```

### 3.6 选题生成流程伪代码

```python
class TopicWorkflowService:
    async def run(self, project_id: int) -> dict:
        raw_hot_topics = await hot_topics_tool.fetch(project_id)
        competitor_posts = await competitor_fetcher.fetch(project_id)
        deduped_inputs = deduplicator.merge(raw_hot_topics, competitor_posts)
        topic_candidates = await topic_agent.generate_candidates(project_id, deduped_inputs)
        saved = topic_repo.bulk_create(project_id, topic_candidates)
        return {"project_id": project_id, "count": len(saved)}
```

### 3.7 Celery 任务样例

`app/tasks/topic_tasks.py`

```python
from app.tasks.celery_app import celery_app


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def generate_daily_topics(self, project_id: int) -> dict:
    from app.services.workflows.topic_workflow import TopicWorkflowService

    service = TopicWorkflowService()
    return service.run_sync(project_id)
```

### 3.8 项目初始化命令

建议初始化步骤：

```bash
mkdir backend
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy psycopg[binary] alembic pydantic-settings redis celery openai playwright
pip freeze > requirements.txt
alembic init alembic
playwright install
```

如果你用 `pyproject.toml` 管理，也可以直接：

```bash
mkdir backend
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install hatchling
```

### 3.9 第一阶段开发任务单

第一阶段建议直接拆成以下任务：

1. 初始化 `FastAPI` 项目骨架
2. 建立 `SQLAlchemy Base` 和数据库连接
3. 建立 `Project`、`BrandProfile`、`TopicCandidate`、`ContentTask`、`ContentAsset` 模型
4. 跑通 `Alembic` 首个迁移
5. 接入阿里百炼 `LLMGateway`
6. 完成项目和品牌配置 API
7. 完成选题生成工作流和异步任务
8. 完成内容生成工作流最小闭环

### 3.10 当前架构决策

第一版明确采用以下原则：

- 工作流优先，不先上重型 agent 框架
- 业务智能体自己开发，底层基础设施复用成熟库
- 所有模型调用统一封装，不在业务代码中直接散调 SDK
- 所有内容发布默认保留人工审核节点
- 先做公众号和小红书，不做泛平台铺开

## 4. 下一步建议

继续往下时，建议优先补这 4 项：

1. 完整 SQLAlchemy 模型和 Alembic 初始迁移
2. FastAPI `main.py`、`config.py`、`db.py` 骨架
3. `LLMGateway` 和 prompt 模板目录
4. `TopicWorkflowService` 与 `WriterAgent` 第一版代码
