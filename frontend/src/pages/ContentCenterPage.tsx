import { useMemo, useState } from "react";

import { EmptyState, PlatformBadge, StatusBadge } from "../components/ui";
import { formatDateTime, formatWorkflowLabel } from "../helpers";
import type { ContentAsset, ContentTask } from "../types";

export function ContentCenterPage({
  tasks,
  selectedTaskId,
  onSelectTaskId,
  assets,
  busy,
  onReview,
  loading,
}: {
  tasks: ContentTask[];
  selectedTaskId: number | null;
  onSelectTaskId: (value: number) => void;
  assets: ContentAsset[];
  busy: string | null;
  onReview: (assetId: number, approved: boolean) => Promise<void>;
  loading: boolean;
}) {
  const [search, setSearch] = useState("");
  const [detailTask, setDetailTask] = useState<ContentTask | null>(null);
  const [detailAsset, setDetailAsset] = useState<ContentAsset | null>(null);

  const filteredTasks = useMemo(() => {
    const keyword = search.trim().toLowerCase();
    return tasks.filter((task) => {
      return (
        keyword === "" ||
        String(task.id).includes(keyword) ||
        String(task.topic_id).includes(keyword) ||
        task.workflow_type.toLowerCase().includes(keyword)
      );
    });
  }, [search, tasks]);

  const currentAssets = detailTask && selectedTaskId === detailTask.id ? assets : [];

  function handleOpenAssets(task: ContentTask) {
    setDetailTask(task);
    onSelectTaskId(task.id);
  }

  function handleOpenAssetDetail(asset: ContentAsset) {
    setDetailAsset(asset);
  }

  return (
    <div className="project-page">
      <div className="table-page-shell">
        <div className="table-page-toolbar">
          <div className="table-page-title">
            <div className="page-breadcrumb">内容管理 / 内容工单</div>
            <h1>内容工单</h1>
          </div>
        </div>

        <div className="table-shell table-shell-strong">
          <div className="table-toolbar">
            <div className="table-toolbar-left">
              <span className="table-toolbar-title">工单列表</span>
            </div>
            <div className="table-toolbar-right table-toolbar-search">
              <input
                className="app-input app-input-search"
                placeholder="搜索工单 ID / Topic ID / 流程类型"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
              />
            </div>
          </div>

          {filteredTasks.length === 0 ? (
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
                  <th>更新时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {filteredTasks.map((task) => (
                  <tr key={task.id} className={selectedTaskId === task.id ? "active" : ""}>
                    <td>#{task.id}</td>
                    <td>#{task.topic_id}</td>
                    <td>{formatWorkflowLabel(task.workflow_type)}</td>
                    <td>
                      <StatusBadge value={task.status} />
                    </td>
                    <td>{formatDateTime(task.updated_at)}</td>
                    <td>
                      <div className="table-action-row">
                        <button className="table-text-button" onClick={() => handleOpenAssets(task)}>
                          查看资产
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
                <h3>工单资产</h3>
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
                  <span className="table-toolbar-title">资产列表</span>
                </div>
              </div>

              {loading && selectedTaskId === detailTask.id ? (
                <div className="table-empty-wrap">
                  <EmptyState text="正在加载资产..." />
                </div>
              ) : currentAssets.length === 0 ? (
                <div className="table-empty-wrap">
                  <EmptyState text="当前工单下没有资产。" />
                </div>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>平台</th>
                      <th>标题</th>
                      <th>摘要</th>
                      <th>审核状态</th>
                      <th>操作</th>
                    </tr>
                  </thead>
                  <tbody>
                    {currentAssets.map((asset) => (
                      <tr key={asset.id}>
                        <td>
                          <PlatformBadge value={asset.platform} />
                        </td>
                        <td>{asset.title || "未命名"}</td>
                        <td className="table-goal-cell">{asset.summary || "未填写"}</td>
                        <td>
                          <StatusBadge value={asset.review_status} />
                        </td>
                        <td>
                          <div className="table-action-row">
                            <button className="table-text-button" onClick={() => handleOpenAssetDetail(asset)}>
                              查看内容
                            </button>
                            <button
                              className="table-text-button"
                              onClick={() => void onReview(asset.id, true)}
                              disabled={busy === `review-${asset.id}`}
                            >
                              通过
                            </button>
                            <button
                              className="table-text-button danger"
                              onClick={() => void onReview(asset.id, false)}
                              disabled={busy === `review-${asset.id}`}
                            >
                              驳回
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
        </div>
      ) : null}

      {detailAsset ? (
        <div className="modal-backdrop" onClick={() => setDetailAsset(null)}>
          <div className="modal-card modal-card-wide" onClick={(event) => event.stopPropagation()}>
            <div className="modal-head">
              <div>
                <h3>生成内容</h3>
                <p>{detailAsset.title || "未命名内容"}</p>
              </div>
              <button className="modal-close" onClick={() => setDetailAsset(null)}>
                关闭
              </button>
            </div>

            <div className="summary-list">
              <div className="summary-line">
                <span>平台</span>
                <strong>
                  <PlatformBadge value={detailAsset.platform} />
                </strong>
              </div>
              <div className="summary-line">
                <span>审核状态</span>
                <strong>
                  <StatusBadge value={detailAsset.review_status} />
                </strong>
              </div>
              <div className="summary-line summary-line-multi">
                <span>摘要</span>
                <strong>{detailAsset.summary || "未填写"}</strong>
              </div>
              <div className="summary-line summary-line-multi">
                <span>封面文案</span>
                <strong>{detailAsset.cover_text || "未填写"}</strong>
              </div>
              <div className="summary-line summary-line-multi">
                <span>CTA</span>
                <strong>{detailAsset.cta_text || "未填写"}</strong>
              </div>
            </div>

            {detailAsset.tags_json && detailAsset.tags_json.length > 0 ? (
              <div className="chip-row">
                {detailAsset.tags_json.map((tag) => (
                  <span key={tag} className="chip">
                    {tag}
                  </span>
                ))}
              </div>
            ) : null}

            <div className="content-box">{detailAsset.content_markdown || "暂无正文内容"}</div>
          </div>
        </div>
      ) : null}
    </div>
  );
}
