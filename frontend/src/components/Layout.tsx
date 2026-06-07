import { useState } from "react";
import { NavLink, Outlet } from "react-router-dom";

import type { BrandProfile, DashboardOverview, Project } from "../types";
import { NoticeBanner } from "./ui";

const NAV_ITEMS = [
  { to: "/", label: "工作台" },
  { to: "/projects", label: "项目管理" },
  { to: "/strategy", label: "品牌策略" },
  { to: "/topics", label: "选题中心" },
  { to: "/contents", label: "内容工单" },
  { to: "/media", label: "素材中心" },
  { to: "/publish", label: "发布中心" },
];

function getStage(brandProfile: BrandProfile | null, dashboard: DashboardOverview | null) {
  if (!brandProfile?.brand_name) return "待完善品牌策略";
  if ((dashboard?.topic_count ?? 0) === 0) return "待生成选题";
  if ((dashboard?.pending_review_count ?? 0) > 0) return "待审核内容";
  if ((dashboard?.published_job_count ?? 0) === 0) return "待执行发布";
  return "已进入复盘阶段";
}

export function Layout({
  projects,
  selectedProjectId,
  onSelectProjectId,
  selectedProject,
  brandProfile,
  dashboard,
  loadingProjects,
  loadingProjectContext,
  notice,
}: {
  projects: Project[];
  selectedProjectId: number | null;
  onSelectProjectId: (value: number) => void;
  selectedProject: Project | null;
  brandProfile: BrandProfile | null;
  dashboard: DashboardOverview | null;
  loadingProjects: boolean;
  loadingProjectContext: boolean;
  notice: { type: "success" | "error"; text: string } | null;
}) {
  const [openUserMenu, setOpenUserMenu] = useState(false);
  const [openProjectMenu, setOpenProjectMenu] = useState(false);

  return (
    <div className="admin-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="brand-mark">CO</div>
          <div>
            <strong>Content Orbit</strong>
            <p>内容自动化后台</p>
          </div>
        </div>

        <nav className="sidebar-nav" aria-label="主导航">
          {NAV_ITEMS.map((item) => (
            <NavLink key={item.to} to={item.to} end={item.to === "/"} className="sidebar-link">
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-user-card">
          <button className="user-trigger" onClick={() => setOpenUserMenu((value) => !value)}>
            <div className="user-avatar">
              <span>LN</span>
              <i className="user-avatar-dot" />
            </div>
            <div className="user-meta">
              <strong>林南</strong>
              <span>管理员</span>
            </div>
            <span className="user-caret">{openUserMenu ? "▴" : "▾"}</span>
          </button>

          {openUserMenu ? (
            <div className="user-dropdown">
              <button className="user-dropdown-item">个人设置</button>
              <button className="user-dropdown-item">账号信息</button>
              <button className="user-dropdown-item danger">退出登录</button>
            </div>
          ) : null}
        </div>
      </aside>

      <div className="admin-main">
        <header className="admin-topbar">
          <div className="admin-topbar-spacer" />

          <div className="admin-topbar-tools">
            <div className="topbar-project-switcher">
              <button
                className="topbar-project-trigger"
                onClick={() => setOpenProjectMenu((value) => !value)}
                disabled={loadingProjects || projects.length === 0}
              >
                <span className="topbar-project-label">当前项目</span>
                <strong>{selectedProject?.name ?? "未选择项目"}</strong>
                <span className="topbar-project-caret">{openProjectMenu ? "▴" : "▾"}</span>
              </button>

              {openProjectMenu ? (
                <div className="topbar-project-dropdown">
                  {projects.length === 0 ? (
                    <div className="topbar-project-empty">暂无项目</div>
                  ) : (
                    projects.map((project) => (
                      <button
                        key={project.id}
                        className={
                          project.id === selectedProjectId
                            ? "topbar-project-item active"
                            : "topbar-project-item"
                        }
                        onClick={() => {
                          onSelectProjectId(project.id);
                          setOpenProjectMenu(false);
                        }}
                      >
                        <strong>{project.name}</strong>
                        <span>{project.industry || "未设置行业"}</span>
                      </button>
                    ))
                  )}
                </div>
              ) : null}
            </div>

            {loadingProjectContext ? <span className="topbar-loading-tag">加载中</span> : null}
          </div>
        </header>

        {notice ? <NoticeBanner type={notice.type} text={notice.text} /> : null}

        <main className="content-area">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
