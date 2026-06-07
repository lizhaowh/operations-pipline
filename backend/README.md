# Content Automation Backend

## Quick Start

1. Create a virtual environment.
2. Install dependencies from `pyproject.toml`.
3. Copy `.env.example` to `.env` and fill in the DashScope key.
4. Ensure PostgreSQL is running and `DATABASE_URL` is valid.
5. Initialize schema with Alembic:

```bash
alembic upgrade head
```

6. Start the API with:

```bash
uvicorn app.main:app --reload
```

7. Seed demo data if you want a ready-to-view workspace:

```bash
python -m app.seed_demo
```

## Included in This Scaffold

- FastAPI app entrypoint
- Settings management via `pydantic-settings`
- SQLAlchemy base/session setup
- Core models for projects, brand profiles, topics, content tasks, and content assets
- Repositories for the first CRUD flows
- Topic generation workflow scaffold
- DashScope-compatible LLM gateway
- Celery app scaffold
- Demo seed script for a complete sample workspace

## Current API

- `GET /health`
- `POST /api/v1/projects`
- `GET /api/v1/projects`
- `GET /api/v1/projects/{project_id}`
- `POST /api/v1/brand-profiles`
- `GET /api/v1/brand-profiles/projects/{project_id}`
- `POST /api/v1/topics/projects/{project_id}/generate`
- `GET /api/v1/topics/projects/{project_id}`
- `POST /api/v1/contents/generate`
- `GET /api/v1/contents/projects/{project_id}/tasks`
- `GET /api/v1/contents/tasks/{task_id}`
- `GET /api/v1/contents/tasks/{task_id}/assets`
- `GET /api/v1/contents/tasks/{task_id}/detail`
- `POST /api/v1/review/assets/{asset_id}`
- `POST /api/v1/publish/jobs`
- `POST /api/v1/publish/jobs/{job_id}/run`
- `GET /api/v1/publish/jobs/{job_id}`
- `GET /api/v1/publish/assets/{asset_id}/assist-preview`
- `POST /api/v1/publish/assets/{asset_id}/assist-run`
- `GET /api/v1/dashboard/projects/{project_id}`
- `GET /api/v1/media/projects/{project_id}`
- `GET /api/v1/media/tasks/{task_id}`
- `POST /api/v1/media/content-assets/{content_asset_id}/generate`

## Publish Modes

- `manual_export`: returns a structured export package for copy/paste publishing
- `assisted_publish`: returns a publish checklist and form payload for operator-assisted posting

## Publisher Layer

- `app/services/publishers/manual_export.py`: builds copy/paste export packages
- `app/services/publishers/playwright_assisted.py`: builds Playwright-assisted runbooks and payloads
- `app/services/publishers/playwright_runner.py`: future browser automation entry scaffold
- `app/services/publishers/factory.py`: resolves publish mode to publisher implementation

## Xiaohongshu Assisted Publish

- first platform-specific scaffold is `xiaohongshu`
- includes creator URL, selector map, and assisted runbook payload
- still stops before actual publish confirmation; this is intentional for safety and stability
- preview endpoint returns environment checks, storage state readiness, and planned selectors before execution

## Media Layer

- `media_assets` table stores generated image assets for each content task
- seed data now includes demo cover images for WeChat and Xiaohongshu assets
- media generation endpoint currently creates demo SVG preview assets for backend workflow validation
