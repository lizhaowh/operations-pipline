import type { ChangeEvent } from "react";
import { useState } from "react";

import { EmptyState, PlatformBadge, PublishModeBadge, StatusBadge } from "../components/ui";
import { formatPlatformLabel, formatWorkflowLabel } from "../helpers";
import type {
  ContentAsset,
  ContentTask,
  PublishExecutionPreview,
  PublishExecutionRun,
  PublishJob,
  PublishResult,
} from "../types";

type PublishRawPayload = {
  mode?: string;
  platform?: string;
  export_package?: {
    title?: string | null;
    summary?: string | null;
    cover_text?: string | null;
    tags?: string[];
    content_markdown?: string | null;
    cta_text?: string | null;
  };
  next_steps?: string[];
  form_payload?: Record<string, unknown>;
  automation?: Record<string, unknown>;
  assistant_steps?: string[];
};

type PackageDetailState = {
  asset: ContentAsset;
  result: PublishResult;
};

export function PublishCenterPage({
  tasks,
  selectedTaskId,
  onSelectTaskId,
  assets,
  publishJobs,
  publishResults,
  publishModes,
  onPublishModeChange,
  assistPreviews,
  assistRuns,
  onCreatePublishJob,
  onRunPublishJob,
  onLoadAssistPreview,
  onRunAssistExecution,
  busy,
}: {
  tasks: ContentTask[];
  selectedTaskId: number | null;
  onSelectTaskId: (value: number) => void;
  assets: ContentAsset[];
  publishJobs: Record<number, PublishJob>;
  publishResults: Record<number, PublishResult>;
  publishModes: Record<number, string>;
  onPublishModeChange: (assetId: number, value: string) => void;
  assistPreviews: Record<number, PublishExecutionPreview>;
  assistRuns: Record<number, PublishExecutionRun>;
  onCreatePublishJob: (assetId: number, publishMode: string) => Promise<void>;
  onRunPublishJob: (assetId: number) => Promise<void>;
  onLoadAssistPreview: (assetId: number) => Promise<void>;
  onRunAssistExecution: (assetId: number) => Promise<void>;
  busy: string | null;
}) {
  const [detailTask, setDetailTask] = useState<ContentTask | null>(null);
  const [packageDetail, setPackageDetail] = useState<PackageDetailState | null>(null);

  const currentAssets =
    detailTask && selectedTaskId === detailTask.id
      ? assets.filter((asset) => asset.review_status === "approved")
      : [];

  function handleOpenPublish(task: ContentTask) {
    setDetailTask(task);
    onSelectTaskId(task.id);
  }

  function handleOpenPackage(asset: ContentAsset, result: PublishResult) {
    setPackageDetail({ asset, result });
  }

  return (
    <div className="project-page">
      <div className="table-page-shell">
        <div className="table-page-toolbar">
          <div className="table-page-title">
            <div className="page-breadcrumb">内容管理 / 发布中心</div>
            <h1>发布中心</h1>
          </div>
        </div>

        <div className="table-shell table-shell-strong">
          <div className="table-toolbar">
            <div className="table-toolbar-left">
              <span className="table-toolbar-title">工单列表</span>
            </div>
          </div>

          {tasks.length === 0 ? (
            <div className="table-empty-wrap">
              <EmptyState text="暂无内容工单。" />
            </div>
          ) : (
            <table className="data-table">
              <thead>
                <tr>
                  <th>工单编号</th>
                  <th>Topic</th>
                  <th>流程类型</th>
                  <th>状态</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {tasks.map((task) => (
                  <tr key={task.id} className={selectedTaskId === task.id ? "active" : ""}>
                    <td>#{task.id}</td>
                    <td>#{task.topic_id}</td>
                    <td>{formatWorkflowLabel(task.workflow_type)}</td>
                    <td>
                      <StatusBadge value={task.status} />
                    </td>
                    <td>
                      <div className="table-action-row">
                        <button className="table-text-button" onClick={() => handleOpenPublish(task)}>
                          查看发布
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {detailTask ? (
        <div className="modal-backdrop" onClick={() => setDetailTask(null)}>
          <div className="modal-card modal-card-wide" onClick={(event) => event.stopPropagation()}>
            <div className="modal-head">
              <div>
                <h3>发布资产</h3>
                <p>工单 #{detailTask.id}</p>
              </div>
              <button className="modal-close" onClick={() => setDetailTask(null)}>
                关闭
              </button>
            </div>

            <div className="summary-list">
              <div className="summary-line">
                <span>工单编号</span>
                <strong>#{detailTask.id}</strong>
              </div>
              <div className="summary-line">
                <span>关联 Topic</span>
                <strong>#{detailTask.topic_id}</strong>
              </div>
              <div className="summary-line">
                <span>流程类型</span>
                <strong>{formatWorkflowLabel(detailTask.workflow_type)}</strong>
              </div>
              <div className="summary-line">
                <span>状态</span>
                <strong>
                  <StatusBadge value={detailTask.status} />
                </strong>
              </div>
            </div>

            <div className="table-shell table-shell-strong">
              <div className="table-toolbar">
                <div className="table-toolbar-left">
                  <span className="table-toolbar-title">可发布资产</span>
                </div>
              </div>

              {currentAssets.length === 0 ? (
                <div className="table-empty-wrap">
                  <EmptyState text="当前工单下没有已审核通过的资产。" />
                </div>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>平台</th>
                      <th>标题</th>
                      <th>发布模式</th>
                      <th>发布任务</th>
                      <th>结果</th>
                      <th>操作</th>
                    </tr>
                  </thead>
                  <tbody>
                    {currentAssets.map((asset) => {
                      const publishMode = publishModes[asset.id] ?? "manual_export";
                      const job = publishJobs[asset.id];
                      const result = publishResults[asset.id];
                      const preview = assistPreviews[asset.id];
                      const assistRun = assistRuns[asset.id];
                      const raw = result?.raw_response_json as PublishRawPayload | undefined;

                      return (
                        <tr key={asset.id}>
                          <td>
                            <PlatformBadge value={asset.platform} />
                          </td>
                          <td>{asset.title ?? `${formatPlatformLabel(asset.platform)} 资产`}</td>
                          <td>
                            <select
                              className="app-select app-select-inline"
                              value={publishMode}
                              onChange={(event: ChangeEvent<HTMLSelectElement>) =>
                                onPublishModeChange(asset.id, event.target.value)
                              }
                            >
                              <option value="manual_export">人工导出</option>
                              <option value="assisted_publish">辅助发布</option>
                            </select>
                          </td>
                          <td>
                            {job ? (
                              <div className="table-cell-stack">
                                <PublishModeBadge value={job.publish_mode} />
                                <StatusBadge value={job.status} />
                              </div>
                            ) : (
                              "未创建"
                            )}
                          </td>
                          <td className="table-goal-cell">
                            {raw?.mode === "manual_export"
                              ? "已生成人工导出包"
                              : raw?.mode === "assisted_publish"
                                ? "已生成辅助发布包"
                                : preview
                                  ? "已完成辅助预检"
                                  : assistRun
                                    ? `执行结果：${assistRun.status}`
                                    : "未生成"}
                          </td>
                          <td>
                            <div className="table-action-row">
                              <button
                                className="table-text-button"
                                onClick={() => void onCreatePublishJob(asset.id, publishMode)}
                                disabled={busy === `job-${asset.id}`}
                              >
                                创建任务
                              </button>
                              <button
                                className="table-text-button"
                                onClick={() => void onRunPublishJob(asset.id)}
                                disabled={!job || busy === `publish-${asset.id}`}
                              >
                                生成发布包
                              </button>
                              <button
                                className="table-text-button"
                                onClick={() => void onLoadAssistPreview(asset.id)}
                                disabled={publishMode !== "assisted_publish"}
                              >
                                预检
                              </button>
                              <button
                                className="table-text-button"
                                onClick={() => void onRunAssistExecution(asset.id)}
                                disabled={publishMode !== "assisted_publish"}
                              >
                                执行
                              </button>
                              <button
                                className="table-text-button"
                                onClick={() => result && handleOpenPackage(asset, result)}
                                disabled={!result}
                              >
                                查看发布包
                              </button>
                            </div>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        </div>
      ) : null}

      {packageDetail ? (
        <div className="modal-backdrop" onClick={() => setPackageDetail(null)}>
          <div className="modal-card modal-card-wide" onClick={(event) => event.stopPropagation()}>
            <div className="modal-head">
              <div>
                <h3>发布包详情</h3>
                <p>{packageDetail.asset.title || "未命名内容"}</p>
              </div>
              <button className="modal-close" onClick={() => setPackageDetail(null)}>
                关闭
              </button>
            </div>

            <PublishPackageDetail asset={packageDetail.asset} result={packageDetail.result} />
          </div>
        </div>
      ) : null}
    </div>
  );
}

function PublishPackageDetail({
  asset,
  result,
}: {
  asset: ContentAsset;
  result: PublishResult;
}) {
  const raw = (result.raw_response_json ?? {}) as PublishRawPayload;
  const exportPackage = raw.export_package;
  const nextSteps = raw.next_steps ?? [];
  const assistantSteps = raw.assistant_steps ?? [];

  return (
    <div className="page-stack">
      <div className="summary-list">
        <div className="summary-line">
          <span>平台</span>
          <strong>
            <PlatformBadge value={asset.platform} />
          </strong>
        </div>
        <div className="summary-line">
          <span>发布模式</span>
          <strong>
            <PublishModeBadge value={raw.mode ?? "manual_export"} />
          </strong>
        </div>
        <div className="summary-line">
          <span>发布结果 ID</span>
          <strong>#{result.id}</strong>
        </div>
      </div>

      {exportPackage ? (
        <>
          <div className="summary-list">
            <div className="summary-line summary-line-multi">
              <span>标题</span>
              <strong>{exportPackage.title || "未填写"}</strong>
            </div>
            <div className="summary-line summary-line-multi">
              <span>摘要</span>
              <strong>{exportPackage.summary || "未填写"}</strong>
            </div>
            <div className="summary-line summary-line-multi">
              <span>封面文案</span>
              <strong>{exportPackage.cover_text || "未填写"}</strong>
            </div>
            <div className="summary-line summary-line-multi">
              <span>CTA</span>
              <strong>{exportPackage.cta_text || "未填写"}</strong>
            </div>
          </div>

          {exportPackage.tags && exportPackage.tags.length > 0 ? (
            <div className="chip-row">
              {exportPackage.tags.map((tag) => (
                <span key={tag} className="chip">
                  {tag}
                </span>
              ))}
            </div>
          ) : null}

          <div className="content-box">{exportPackage.content_markdown || "暂无正文内容"}</div>

          {nextSteps.length > 0 ? (
            <div className="summary-list">
              {nextSteps.map((step, index) => (
                <div key={`${index}-${step}`} className="summary-line summary-line-multi">
                  <span>步骤 {index + 1}</span>
                  <strong>{step}</strong>
                </div>
              ))}
            </div>
          ) : null}
        </>
      ) : null}

      {raw.form_payload ? (
        <>
          <div className="summary-line summary-line-multi">
            <span>辅助发布表单</span>
            <strong>以下内容将用于自动填充发布页面</strong>
          </div>
          <div className="content-box compact">{JSON.stringify(raw.form_payload, null, 2)}</div>
        </>
      ) : null}

      {raw.automation ? (
        <>
          <div className="summary-line summary-line-multi">
            <span>自动化配置</span>
            <strong>Playwright 辅助发布运行配置</strong>
          </div>
          <div className="content-box compact">{JSON.stringify(raw.automation, null, 2)}</div>
        </>
      ) : null}

      {assistantSteps.length > 0 ? (
        <div className="summary-list">
          {assistantSteps.map((step, index) => (
            <div key={`${index}-${step}`} className="summary-line summary-line-multi">
              <span>辅助步骤 {index + 1}</span>
              <strong>{step}</strong>
            </div>
          ))}
        </div>
      ) : null}
    </div>
  );
}
