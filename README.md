# operations-pipline

一个面向内容生产场景的运营自动化项目，当前仓库包含：

- `backend/`：基于 Python 的后端服务与数据模型
- `frontend/`：基于 Vite 的前端界面
- `docs/`：产品方案与设计文档

## 功能方向

项目当前聚焦内容生产 MVP，覆盖这些核心流程：

- 选题管理
- 内容生成
- 媒体素材管理
- 审核与发布
- 数据看板

## 目录结构

```text
.
|-- backend
|-- frontend
`-- docs
```

## 本地开发

### Backend

进入 `backend/` 后按 Python 项目方式安装依赖并启动服务。

### Frontend

进入 `frontend/` 后执行：

```bash
npm install
npm run dev
```

## 环境变量

- 后端示例配置：`backend/.env.example`
- 前端示例配置：`frontend/.env.example`

## 说明

这是一个初始版本仓库，README 目前保持简洁，后续可以再补充接口说明、部署方式和开发规范。
