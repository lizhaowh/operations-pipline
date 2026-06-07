import { useEffect, useState } from "react";

import { EmptyState, StatusBadge } from "../components/ui";
import { formatDateTime, formatTopicSourceLabel } from "../helpers";
import type { Topic } from "../types";

export function TopicsPage({
  topics,
  selectedTopicId,
  onSelectTopicId,
  onGenerateTopics,
  onDeleteTopic,
  onGenerateContent,
  busy,
  selectedProjectId,
}: {
  topics: Topic[];
  selectedTopicId: number | null;
  onSelectTopicId: (value: number) => void;
  onGenerateTopics: () => Promise<void>;
  onDeleteTopic: (topicId: number) => Promise<void>;
  onGenerateContent: () => Promise<void>;
  busy: string | null;
  selectedProjectId: number | null;
}) {
  const [detailTopic, setDetailTopic] = useState<Topic | null>(null);

  useEffect(() => {
    if (detailTopic == null) return;
    const nextDetail = topics.find((topic) => topic.id === detailTopic.id) ?? null;
    setDetailTopic(nextDetail);
  }, [detailTopic, topics]);

  function handleView(topic: Topic) {
    onSelectTopicId(topic.id);
    setDetailTopic(topic);
  }

  async function handleDelete(topic: Topic) {
    await onDeleteTopic(topic.id);
    if (detailTopic?.id === topic.id) {
      setDetailTopic(null);
    }
  }

  return (
    <div className="project-page">
      <div className="table-page-shell">
        <div className="table-page-toolbar">
          <div className="table-page-title">
            <div className="page-breadcrumb">内容管理 / 选题中心</div>
            <h1>选题中心</h1>
          </div>
        </div>

        <div className="table-shell table-shell-strong">
          <div className="table-toolbar">
            <div className="table-toolbar-left">
              <span className="table-toolbar-title">选题列表</span>
            </div>
            <div className="table-toolbar-right">
              <button
                className="table-text-button"
                onClick={() => void onGenerateTopics()}
                disabled={selectedProjectId == null || busy === "topics"}
              >
                {busy === "topics" ? "生成中..." : "生成选题"}
              </button>
            </div>
          </div>

          {topics.length === 0 ? (
            <div className="table-empty-wrap">
              <EmptyState text="暂无选题，请先生成选题。" />
            </div>
          ) : (
            <table className="data-table">
              <thead>
                <tr>
                  <th>选题标题</th>
                  <th>角度</th>
                  <th>来源</th>
                  <th>综合分</th>
                  <th>状态</th>
                  <th>创建时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {topics.map((topic) => (
                  <tr key={topic.id} className={selectedTopicId === topic.id ? "active" : ""}>
                    <td>{topic.title}</td>
                    <td className="table-goal-cell">{topic.angle || "未填写"}</td>
                    <td>{formatTopicSourceLabel(topic.source_type)}</td>
                    <td>{topic.final_score.toFixed(1)}</td>
                    <td>
                      <StatusBadge value={topic.status} />
                    </td>
                    <td>{formatDateTime(topic.created_at)}</td>
                    <td>
                      <div className="table-action-row">
                        <button className="table-text-button" onClick={() => handleView(topic)}>
                          查看
                        </button>
                        <button
                          className="table-text-button"
                          onClick={() => {
                            onSelectTopicId(topic.id);
                            void onGenerateContent();
                          }}
                          disabled={busy === "content"}
                        >
                          {busy === "content" && selectedTopicId === topic.id ? "生成中..." : "生成工单"}
                        </button>
                        <button
                          className="table-text-button"
                          onClick={() => void handleDelete(topic)}
                          disabled={busy === `topic-delete-${topic.id}`}
                        >
                          {busy === `topic-delete-${topic.id}` ? "删除中..." : "删除"}
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

      {detailTopic ? (
        <div className="modal-backdrop" onClick={() => setDetailTopic(null)}>
          <div className="modal-card" onClick={(event) => event.stopPropagation()}>
            <div className="modal-head">
              <div>
                <h3>选题详情</h3>
              </div>
              <button className="modal-close" onClick={() => setDetailTopic(null)}>
                关闭
              </button>
            </div>

            <div className="summary-list">
              <div className="summary-line summary-line-multi">
                <span>选题标题</span>
                <strong>{detailTopic.title}</strong>
              </div>
              <div className="summary-line summary-line-multi">
                <span>内容角度</span>
                <strong>{detailTopic.angle || "未填写"}</strong>
              </div>
              <div className="summary-line">
                <span>来源</span>
                <strong>{formatTopicSourceLabel(detailTopic.source_type)}</strong>
              </div>
              <div className="summary-line">
                <span>热度分</span>
                <strong>{detailTopic.heat_score.toFixed(1)}</strong>
              </div>
              <div className="summary-line">
                <span>相关性分</span>
                <strong>{detailTopic.relevance_score.toFixed(1)}</strong>
              </div>
              <div className="summary-line">
                <span>转化分</span>
                <strong>{detailTopic.conversion_score.toFixed(1)}</strong>
              </div>
              <div className="summary-line">
                <span>竞争度分</span>
                <strong>{detailTopic.competition_score.toFixed(1)}</strong>
              </div>
              <div className="summary-line">
                <span>综合分</span>
                <strong>{detailTopic.final_score.toFixed(1)}</strong>
              </div>
              <div className="summary-line summary-line-multi">
                <span>推荐理由</span>
                <strong>{detailTopic.reason || "暂无推荐理由"}</strong>
              </div>
              <div className="summary-line">
                <span>创建时间</span>
                <strong>{formatDateTime(detailTopic.created_at)}</strong>
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}
