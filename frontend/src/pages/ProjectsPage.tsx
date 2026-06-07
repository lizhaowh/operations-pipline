import type { FormEvent } from "react";
import { useState } from "react";

import { EmptyState, StatusBadge } from "../components/ui";
import { formatDateTime } from "../helpers";
import type { Project } from "../types";

type ProjectFormState = {
  name: string;
  industry: string;
  goal: string;
};

export function ProjectsPage({
  projects,
  selectedProjectId,
  onSelectProjectId,
  projectForm,
  onProjectFormChange,
  onCreateProject,
  onUpdateProject,
  onDeleteProject,
  busy,
}: {
  projects: Project[];
  selectedProjectId: number | null;
  onSelectProjectId: (value: number) => void;
  projectForm: ProjectFormState;
  onProjectFormChange: (key: keyof ProjectFormState, value: string) => void;
  onCreateProject: (event: FormEvent) => Promise<void>;
  onUpdateProject: (projectId: number, event: FormEvent) => Promise<void>;
  onDeleteProject: (projectId: number) => Promise<void>;
  busy: string | null;
}) {
  const [openCreateModal, setOpenCreateModal] = useState(false);
  const [openEditModal, setOpenEditModal] = useState(false);
  const [detailProject, setDetailProject] = useState<Project | null>(null);
  const [editingProject, setEditingProject] = useState<Project | null>(null);

  async function handleCreate(event: FormEvent) {
    await onCreateProject(event);
    if (busy !== "project") {
      setOpenCreateModal(false);
    }
  }

  async function handleUpdate(event: FormEvent) {
    if (editingProject == null) return;
    await onUpdateProject(editingProject.id, event);
    if (busy !== "project-update") {
      setOpenEditModal(false);
      setEditingProject(null);
    }
  }

  function handleOpenCreate() {
    onProjectFormChange("name", "");
    onProjectFormChange("industry", "");
    onProjectFormChange("goal", "");
    setOpenCreateModal(true);
  }

  function handleOpenEdit(project: Project) {
    setEditingProject(project);
    onProjectFormChange("name", project.name);
    onProjectFormChange("industry", project.industry ?? "");
    onProjectFormChange("goal", project.goal ?? "");
    setOpenEditModal(true);
  }

  async function handleDelete(project: Project) {
    if (!window.confirm(`确认删除项目“${project.name}”？`)) return;
    await onDeleteProject(project.id);
  }

  return (
    <div className="project-page">
      <div className="table-page-shell">
        <div className="table-page-toolbar">
          <div className="table-page-title">
            <div className="page-breadcrumb">系统管理 / 项目管理</div>
            <h1>项目管理</h1>
          </div>
        </div>

        <div className="table-shell table-shell-strong">
          <div className="table-toolbar">
            <div className="table-toolbar-left">
              <span className="table-toolbar-title">项目列表</span>
            </div>
            <div className="table-toolbar-right">
              <button className="table-text-button" onClick={handleOpenCreate}>
                新建项目
              </button>
            </div>
          </div>

          {projects.length === 0 ? (
            <div className="table-empty-wrap">
              <EmptyState text="暂无项目，请先新建项目。" />
            </div>
          ) : (
            <table className="data-table">
              <thead>
                <tr>
                  <th>项目名称</th>
                  <th>行业赛道</th>
                  <th>业务目标</th>
                  <th>状态</th>
                  <th>创建时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {projects.map((project) => (
                  <tr
                    key={project.id}
                    className={selectedProjectId === project.id ? "active" : ""}
                    onClick={() => onSelectProjectId(project.id)}
                  >
                    <td>
                      <div className="table-primary-cell">
                        <strong>{project.name}</strong>
                      </div>
                    </td>
                    <td>{project.industry || "未填写"}</td>
                    <td className="table-goal-cell">{project.goal || "未填写"}</td>
                    <td>
                      <StatusBadge value={project.status} />
                    </td>
                    <td>{formatDateTime(project.created_at)}</td>
                    <td onClick={(event) => event.stopPropagation()}>
                      <div className="table-action-row">
                        <button className="table-text-button" onClick={() => setDetailProject(project)}>
                          详情
                        </button>
                        <button className="table-text-button" onClick={() => handleOpenEdit(project)}>
                          编辑
                        </button>
                        <button className="table-text-button danger" onClick={() => void handleDelete(project)}>
                          删除
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

      {openCreateModal ? (
        <div className="modal-backdrop" onClick={() => setOpenCreateModal(false)}>
          <div className="modal-card" onClick={(event) => event.stopPropagation()}>
            <div className="modal-head">
              <div>
                <h3>新建项目</h3>
              </div>
              <button className="modal-close" onClick={() => setOpenCreateModal(false)}>
                关闭
              </button>
            </div>

            <form className="form-grid" onSubmit={(event) => void handleCreate(event)}>
              <ProjectFormFields form={projectForm} onChange={onProjectFormChange} />
              <div className="modal-actions">
                <button type="button" className="secondary-button" onClick={() => setOpenCreateModal(false)}>
                  取消
                </button>
                <button className="primary-button" disabled={busy === "project" || !projectForm.name.trim()}>
                  {busy === "project" ? "创建中..." : "确认创建"}
                </button>
              </div>
            </form>
          </div>
        </div>
      ) : null}

      {openEditModal && editingProject ? (
        <div className="modal-backdrop" onClick={() => setOpenEditModal(false)}>
          <div className="modal-card" onClick={(event) => event.stopPropagation()}>
            <div className="modal-head">
              <div>
                <h3>编辑项目</h3>
              </div>
              <button className="modal-close" onClick={() => setOpenEditModal(false)}>
                关闭
              </button>
            </div>

            <form className="form-grid" onSubmit={(event) => void handleUpdate(event)}>
              <ProjectFormFields form={projectForm} onChange={onProjectFormChange} />
              <div className="modal-actions">
                <button type="button" className="secondary-button" onClick={() => setOpenEditModal(false)}>
                  取消
                </button>
                <button className="primary-button" disabled={busy === "project-update" || !projectForm.name.trim()}>
                  {busy === "project-update" ? "保存中..." : "保存"}
                </button>
              </div>
            </form>
          </div>
        </div>
      ) : null}

      {detailProject ? (
        <div className="modal-backdrop" onClick={() => setDetailProject(null)}>
          <div className="modal-card" onClick={(event) => event.stopPropagation()}>
            <div className="modal-head">
              <div>
                <h3>项目详情</h3>
              </div>
              <button className="modal-close" onClick={() => setDetailProject(null)}>
                关闭
              </button>
            </div>

            <div className="summary-list">
              <div className="summary-line">
                <span>项目名称</span>
                <strong>{detailProject.name}</strong>
              </div>
              <div className="summary-line">
                <span>行业赛道</span>
                <strong>{detailProject.industry || "未填写"}</strong>
              </div>
              <div className="summary-line summary-line-multi">
                <span>业务目标</span>
                <strong>{detailProject.goal || "未填写"}</strong>
              </div>
              <div className="summary-line">
                <span>状态</span>
                <strong>{detailProject.status}</strong>
              </div>
              <div className="summary-line">
                <span>创建时间</span>
                <strong>{formatDateTime(detailProject.created_at)}</strong>
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}

function ProjectFormFields({
  form,
  onChange,
}: {
  form: ProjectFormState;
  onChange: (key: keyof ProjectFormState, value: string) => void;
}) {
  return (
    <>
      <label className="field-block" htmlFor="project-name">
        <span>项目名称</span>
        <input
          id="project-name"
          className="app-input"
          placeholder="例如：AI 内容增长引擎"
          value={form.name}
          onChange={(event) => onChange("name", event.target.value)}
        />
      </label>
      <label className="field-block" htmlFor="project-industry">
        <span>行业赛道</span>
        <input
          id="project-industry"
          className="app-input"
          placeholder="例如：企业服务"
          value={form.industry}
          onChange={(event) => onChange("industry", event.target.value)}
        />
      </label>
      <label className="field-block" htmlFor="project-goal">
        <span>业务目标</span>
        <textarea
          id="project-goal"
          className="app-textarea"
          placeholder="例如：稳定产出公众号和小红书内容"
          value={form.goal}
          onChange={(event) => onChange("goal", event.target.value)}
        />
      </label>
    </>
  );
}
