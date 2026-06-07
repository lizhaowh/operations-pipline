# Content Automation Frontend

## Quick Start

1. Copy `.env.example` to `.env`.
2. Set `VITE_API_BASE_URL` to the backend API base URL.
3. Install dependencies:

```bash
npm install
```

4. Start the dev server:

```bash
npm run dev
```

## Current Scope

- Chinese admin-style layout with left sidebar navigation
- Multi-page workflow: `工作台 / 项目管理 / 品牌策略 / 选题中心 / 内容工单 / 素材中心 / 发布中心`
- Project creation and project switching
- Dashboard overview, production funnel, and recent tasks
- Brand profile editing
- Topic generation and topic detail review
- Content task queue and asset review
- Media center for demo cover and image assets
- Publish job creation with `manual_export / assisted_publish`
- Assist preview and assist run entry for supported publishers
