import { formatDateTime, formatWorkflowLabel } from "../helpers";
import { EmptyState, StatusBadge } from "../components/ui";
import type { ContentTask, DashboardOverview, Project } from "../types";
import type { Notice } from "../types-extra";

export function DashboardPage({
  selectedProject,
  dashboard,
  recentTasks,
  notice,
  loading,
}: {
  selectedProject: Project | null;
  dashboard: DashboardOverview | null;
  recentTasks: ContentTask[];
  notice: Notice;
  loading: boolean;
}) {
  return (
    <div className="project-page">
      <div className="table-page-shell">
        <div className="table-page-toolbar">
          <div className="table-page-title">
            <div className="page-breadcrumb">控制台 / 工作台</div>
            <h1>工作台</h1>
          </div>
        </div>

        <div className="dashboard-grid">
          <div className="dashboard-kpi-row">
            <div className="dashboard-kpi-card">
              <span>候选选题</span>
              <strong>{dashboard?.topic_count ?? 0}</strong>
            </div>
            <div className="dashboard-kpi-card">
              <span>内容工单</span>
              <strong>{dashboard?.content_task_count ?? 0}</strong>
            </div>
            <div className="dashboard-kpi-card">
              <span>待审核</span>
              <strong>{dashboard?.pending_review_count ?? 0}</strong>
            </div>
            <div className="dashboard-kpi-card">
              <span>已发布</span>
              <strong>{dashboard?.published_job_count ?? 0}</strong>
            </div>
          </div>

          <div className="dashboard-panel-grid">
            <section className="table-shell table-shell-strong info-shell">
              <div className="table-toolbar">
                <span className="table-toolbar-title">项目摘要</span>
              </div>
              {selectedProject ? (
                <div className="summary-list summary-list-padded">
                  <div className="summary-line">
                    <span>项目名称</span>
                    <strong>{selectedProject.name}</strong>
                  </div>
                  <div className="summary-line">
                    <span>行业赛道</span>
                    <strong>{selectedProject.industry ?? "未填写"}</strong>
                  </div>
                  <div className="summary-line summary-line-multi">
                    <span>业务目标</span>
                    <strong>{selectedProject.goal ?? "未填写"}</strong>
                  </div>
                </div>
              ) : (
                <div className="table-empty-wrap">
                  <EmptyState text="请先在项目管理中选择项目。" />
                </div>
              )}
            </section>

            <section className="table-shell table-shell-strong info-shell">
              <div className="table-toolbar">
                <span className="table-toolbar-title">最近工单</span>
              </div>
              {recentTasks.length === 0 ? (
                <div className="table-empty-wrap">
                  <EmptyState text="暂无内容工单。" />
                </div>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>工单</th>
                      <th>流程</th>
                      <th>状态</th>
                      <th>更新时间</th>
                    </tr>
                  </thead>
                  <tbody>
                    {recentTasks.slice(0, 6).map((task) => (
                      <tr key={task.id}>
                        <td>#{task.id}</td>
                        <td>{formatWorkflowLabel(task.workflow_type)}</td>
                        <td>
                          <StatusBadge value={task.status} />
                        </td>
                        <td>{formatDateTime(task.updated_at)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </section>
          </div>

          {loading ? <div className="inline-tip">正在同步项目数据。</div> : null}
          {notice && notice.type === "error" ? (
            <div className="inline-tip warning">{notice.text}</div>
          ) : null}
        </div>
      </div>
    </div>
  );
}
