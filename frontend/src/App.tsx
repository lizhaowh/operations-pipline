import type { FormEvent } from "react";
import { useEffect, useRef, useState } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import { api } from "./api";
import { Layout } from "./components/Layout";
import {
  fromBrandProfile,
  getErrorMessage,
  parseJsonArrayText,
  parseJsonText,
  parseLines,
} from "./helpers";
import { ContentCenterPage } from "./pages/ContentCenterPage";
import { DashboardPage } from "./pages/DashboardPage";
import { MediaCenterPage } from "./pages/MediaCenterPage";
import { ProjectsPage } from "./pages/ProjectsPage";
import { PublishCenterPage } from "./pages/PublishCenterPage";
import { StrategyPage } from "./pages/StrategyPage";
import { TopicsPage } from "./pages/TopicsPage";
import type {
  BrandProfile,
  ContentAsset,
  ContentTask,
  ContentTaskDetail,
  DashboardOverview,
  MediaAsset,
  Project,
  PublishExecutionPreview,
  PublishExecutionRun,
  PublishJob,
  PublishResult,
  Topic,
} from "./types";
import type { BrandFormState, Notice } from "./types-extra";

const defaultBrandForm: BrandFormState = {
  brand_name: "",
  brand_desc: "",
  target_audience: "",
  tone_of_voice: "",
  product_info_text: "",
  cta_rules_text: "",
  banned_words_text: "",
  competitor_accounts_text: "",
  extra_context: "",
};

function App() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState<number | null>(null);
  const [dashboard, setDashboard] = useState<DashboardOverview | null>(null);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [contentTasks, setContentTasks] = useState<ContentTask[]>([]);
  const [selectedTopicId, setSelectedTopicId] = useState<number | null>(null);
  const [selectedTaskId, setSelectedTaskId] = useState<number | null>(null);
  const [assets, setAssets] = useState<ContentAsset[]>([]);
  const [publishJobs, setPublishJobs] = useState<Record<number, PublishJob>>({});
  const [publishResults, setPublishResults] = useState<Record<number, PublishResult>>({});
  const [publishModes, setPublishModes] = useState<Record<number, string>>({});
  const [assistPreviews, setAssistPreviews] = useState<Record<number, PublishExecutionPreview>>({});
  const [assistRuns, setAssistRuns] = useState<Record<number, PublishExecutionRun>>({});
  const [mediaAssets, setMediaAssets] = useState<MediaAsset[]>([]);
  const [brandProfile, setBrandProfile] = useState<BrandProfile | null>(null);
  const [brandForm, setBrandForm] = useState<BrandFormState>(defaultBrandForm);
  const [projectForm, setProjectForm] = useState({ name: "", industry: "", goal: "" });
  const [notice, setNotice] = useState<Notice>(null);
  const [busy, setBusy] = useState<string | null>(null);
  const [loadingProjects, setLoadingProjects] = useState(true);
  const [loadingProjectContext, setLoadingProjectContext] = useState(false);
  const [loadingTaskDetail, setLoadingTaskDetail] = useState(false);
  const lastProjectIdRef = useRef<number | null>(null);

  useEffect(() => {
    void loadProjects();
  }, []);

  useEffect(() => {
    if (selectedProjectId == null) return;
    const projectChanged = lastProjectIdRef.current !== selectedProjectId;
    if (projectChanged) {
      setAssets([]);
      setPublishJobs({});
      setPublishResults({});
      setPublishModes({});
      setAssistPreviews({});
      setAssistRuns({});
      setMediaAssets([]);
      lastProjectIdRef.current = selectedProjectId;
    }
    void loadProjectContext(selectedProjectId);
  }, [selectedProjectId]);

  useEffect(() => {
    if (selectedTaskId == null) return;
    void loadTaskDetail(selectedTaskId);
  }, [selectedTaskId]);

  async function loadProjects() {
    setLoadingProjects(true);
    try {
      const items = await api.listProjects();
      setProjects(items);
      if (items.length > 0 && selectedProjectId == null) {
        setSelectedProjectId(items[0].id);
      }
    } catch (error) {
      setNotice({ type: "error", text: getErrorMessage(error) });
    } finally {
      setLoadingProjects(false);
    }
  }

  async function loadProjectContext(projectId: number) {
    setLoadingProjectContext(true);
    try {
      const [overview, topicItems, taskItems] = await Promise.all([
        api.getDashboard(projectId),
        api.listTopics(projectId),
        api.listContentTasks(projectId),
      ]);
      setDashboard(overview);
      setTopics(topicItems);
      setContentTasks(taskItems);

      try {
        const profile = await api.getBrandProfile(projectId);
        setBrandProfile(profile);
        setBrandForm(fromBrandProfile(profile));
      } catch {
        setBrandProfile(null);
        setBrandForm(defaultBrandForm);
      }

      setSelectedTopicId((current) =>
        topicItems.some((item) => item.id === current) ? current : (topicItems[0]?.id ?? null),
      );
      setSelectedTaskId((current) =>
        taskItems.some((item) => item.id === current) ? current : (taskItems[0]?.id ?? null),
      );
      if (taskItems.length === 0) {
        setAssets([]);
        setMediaAssets([]);
      }
    } catch (error) {
      setNotice({ type: "error", text: getErrorMessage(error) });
    } finally {
      setLoadingProjectContext(false);
    }
  }

  async function loadTaskDetail(taskId: number) {
    setLoadingTaskDetail(true);
    try {
      const [detail, mediaItems] = await Promise.all([
        api.getContentTaskDetail(taskId),
        api.listMediaByTask(taskId),
      ]);
      setAssets(detail.assets);
      setMediaAssets(mediaItems);
    } catch (error) {
      setNotice({ type: "error", text: getErrorMessage(error) });
    } finally {
      setLoadingTaskDetail(false);
    }
  }

  async function refreshProjectContext() {
    if (selectedProjectId != null) {
      await loadProjectContext(selectedProjectId);
    }
  }

  async function handleProjectCreate(event: FormEvent) {
    event.preventDefault();
    setBusy("project");
    try {
      const created = await api.createProject({
        name: projectForm.name,
        industry: projectForm.industry || undefined,
        goal: projectForm.goal || undefined,
      });
      setProjectForm({ name: "", industry: "", goal: "" });
      setNotice({ type: "success", text: `项目「${created.name}」已创建` });
      await loadProjects();
      setSelectedProjectId(created.id);
    } catch (error) {
      setNotice({ type: "error", text: getErrorMessage(error) });
    } finally {
      setBusy(null);
    }
  }

  async function handleProjectUpdate(projectId: number, event: FormEvent) {
    event.preventDefault();
    setBusy("project-update");
    try {
      const updated = await api.updateProject(projectId, {
        name: projectForm.name,
        industry: projectForm.industry || undefined,
        goal: projectForm.goal || undefined,
      });
      setNotice({ type: "success", text: `项目「${updated.name}」已更新` });
      await loadProjects();
      setSelectedProjectId(updated.id);
    } catch (error) {
      setNotice({ type: "error", text: getErrorMessage(error) });
    } finally {
      setBusy(null);
    }
  }

  async function handleProjectDelete(projectId: number) {
    setBusy(`project-delete-${projectId}`);
    try {
      await api.deleteProject(projectId);
      setNotice({ type: "success", text: "项目已删除" });
      const nextProjects = projects.filter((item) => item.id !== projectId);
      setProjects(nextProjects);
      if (selectedProjectId === projectId) {
        setSelectedProjectId(nextProjects[0]?.id ?? null);
      }
      if (nextProjects.length > 0) {
        await loadProjects();
      } else {
        setDashboard(null);
        setTopics([]);
        setContentTasks([]);
        setAssets([]);
        setMediaAssets([]);
        setBrandProfile(null);
        setBrandForm(defaultBrandForm);
      }
    } catch (error) {
      setNotice({ type: "error", text: getErrorMessage(error) });
    } finally {
      setBusy(null);
    }
  }

  async function handleBrandSave(event: FormEvent) {
    event.preventDefault();
    if (selectedProjectId == null) return;
    setBusy("brand");
    try {
      const saved = await api.upsertBrandProfile({
        project_id: selectedProjectId,
        brand_name: brandForm.brand_name,
        brand_desc: brandForm.brand_desc || null,
        target_audience: brandForm.target_audience || null,
        tone_of_voice: brandForm.tone_of_voice || null,
        product_info_json: parseJsonText(brandForm.product_info_text),
        cta_rules_json: parseJsonText(brandForm.cta_rules_text),
        banned_words_json: parseLines(brandForm.banned_words_text),
        competitor_accounts_json: parseJsonArrayText(brandForm.competitor_accounts_text),
        extra_context: brandForm.extra_context || null,
      });
      setBrandProfile(saved);
      setNotice({ type: "success", text: "品牌策略已保存" });
    } catch (error) {
      setNotice({ type: "error", text: getErrorMessage(error) });
    } finally {
      setBusy(null);
    }
  }

  async function handleGenerateTopics() {
    if (selectedProjectId == null) return;
    setBusy("topics");
    try {
      const result = await api.generateTopics(selectedProjectId);
      await refreshProjectContext();
      setNotice({ type: "success", text: `已生成 ${result.count} 个候选选题` });
    } catch (error) {
      setNotice({ type: "error", text: getErrorMessage(error) });
    } finally {
      setBusy(null);
    }
  }

  async function handleDeleteTopic(topicId: number) {
    if (selectedProjectId == null) return;
    setBusy(`topic-delete-${topicId}`);
    try {
      await api.deleteTopic(selectedProjectId, topicId);
      setTopics((current) => current.filter((item) => item.id !== topicId));
      setSelectedTopicId((current) => (current === topicId ? null : current));
      setNotice({ type: "success", text: `选题 #${topicId} 已删除` });
    } catch (error) {
      setNotice({ type: "error", text: getErrorMessage(error) });
    } finally {
      setBusy(null);
    }
  }

  async function handleGenerateContent() {
    if (selectedTopicId == null) return;
    setBusy("content");
    try {
      const task = await api.generateContent({
        topic_id: selectedTopicId,
        platforms: ["wechat", "xiaohongshu"],
      });
      await refreshProjectContext();
      setSelectedTaskId(task.id);
      await loadTaskDetail(task.id);
      setNotice({ type: "success", text: `内容工单 #${task.id} 已生成` });
    } catch (error) {
      setNotice({ type: "error", text: getErrorMessage(error) });
    } finally {
      setBusy(null);
    }
  }

  async function handleReview(assetId: number, approved: boolean) {
    setBusy(`review-${assetId}`);
    try {
      const updated = await api.reviewAsset(assetId, {
        approved,
        notes: approved ? "审核通过" : "需要重写结构或表达方式",
      });
      setAssets((current) => current.map((asset) => (asset.id === assetId ? updated : asset)));
      await refreshProjectContext();
      if (selectedTaskId != null) {
        await loadTaskDetail(selectedTaskId);
      }
      setNotice({ type: "success", text: approved ? "内容已审核通过" : "内容已驳回" });
    } catch (error) {
      setNotice({ type: "error", text: getErrorMessage(error) });
    } finally {
      setBusy(null);
    }
  }

  async function handleCreatePublishJob(assetId: number, publishMode: string) {
    setBusy(`job-${assetId}`);
    try {
      const job = await api.createPublishJob({
        content_asset_id: assetId,
        publish_mode: publishMode,
        scheduled_at: null,
      });
      setPublishJobs((current) => ({ ...current, [assetId]: job }));
      setNotice({ type: "success", text: `已为资产 #${assetId} 创建发布任务` });
    } catch (error) {
      setNotice({ type: "error", text: getErrorMessage(error) });
    } finally {
      setBusy(null);
    }
  }

  async function handleRunPublishJob(assetId: number) {
    const job = publishJobs[assetId];
    if (!job) return;
    setBusy(`publish-${assetId}`);
    try {
      const result = await api.runPublishJob(job.id);
      const updatedJob = await api.getPublishJob(job.id);
      setPublishResults((current) => ({ ...current, [assetId]: result }));
      setPublishJobs((current) => ({ ...current, [assetId]: updatedJob }));
      setNotice({ type: "success", text: `已生成 ${updatedJob.platform} 的发布材料` });
    } catch (error) {
      setNotice({ type: "error", text: getErrorMessage(error) });
    } finally {
      setBusy(null);
    }
  }

  async function handleLoadAssistPreview(assetId: number) {
    setBusy(`assist-preview-${assetId}`);
    try {
      const preview = await api.getAssistPreview(assetId);
      setAssistPreviews((current) => ({ ...current, [assetId]: preview }));
      setNotice({ type: "success", text: "辅助发布预检已更新" });
    } catch (error) {
      setNotice({ type: "error", text: getErrorMessage(error) });
    } finally {
      setBusy(null);
    }
  }

  async function handleRunAssistExecution(assetId: number) {
    setBusy(`assist-run-${assetId}`);
    try {
      const result = await api.runAssistExecution(assetId);
      setAssistRuns((current) => ({ ...current, [assetId]: result }));
      setNotice({ type: "success", text: "辅助发布执行结果已返回" });
    } catch (error) {
      setNotice({ type: "error", text: getErrorMessage(error) });
    } finally {
      setBusy(null);
    }
  }

  async function handleGenerateMedia(contentAssetId: number) {
    setBusy(`media-${contentAssetId}`);
    try {
      await api.generateMediaForAsset(contentAssetId, { roles: ["cover", "body"] });
      if (selectedTaskId != null) {
        await loadTaskDetail(selectedTaskId);
      }
      setNotice({ type: "success", text: "素材演示图已生成" });
    } catch (error) {
      setNotice({ type: "error", text: getErrorMessage(error) });
    } finally {
      setBusy(null);
    }
  }

  function handleBrandFormChange(key: keyof BrandFormState, value: string) {
    setBrandForm((current) => ({ ...current, [key]: value }));
  }

  function handleProjectFormChange(key: "name" | "industry" | "goal", value: string) {
    setProjectForm((current) => ({ ...current, [key]: value }));
  }

  function handlePublishModeChange(assetId: number, value: string) {
    setPublishModes((current) => ({ ...current, [assetId]: value }));
  }

  const selectedProject = projects.find((item) => item.id === selectedProjectId) ?? null;
  const recentTasks = contentTasks.slice(0, 8);

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <Layout
              projects={projects}
              selectedProjectId={selectedProjectId}
              onSelectProjectId={setSelectedProjectId}
              selectedProject={selectedProject}
              brandProfile={brandProfile}
              dashboard={dashboard}
              loadingProjects={loadingProjects}
              loadingProjectContext={loadingProjectContext}
              notice={notice}
            />
          }
        >
          <Route
            index
            element={
              <DashboardPage
                selectedProject={selectedProject}
                dashboard={dashboard}
                recentTasks={recentTasks}
                notice={notice}
                loading={loadingProjects || loadingProjectContext}
              />
            }
          />
          <Route
            path="projects"
            element={
              <ProjectsPage
                projects={projects}
                selectedProjectId={selectedProjectId}
                onSelectProjectId={setSelectedProjectId}
                projectForm={projectForm}
                onProjectFormChange={handleProjectFormChange}
                onCreateProject={handleProjectCreate}
                onUpdateProject={handleProjectUpdate}
                onDeleteProject={handleProjectDelete}
                busy={busy}
              />
            }
          />
          <Route
            path="strategy"
            element={
              <StrategyPage
                brandProfile={brandProfile}
                brandForm={brandForm}
                onBrandFormChange={handleBrandFormChange}
                onBrandSave={handleBrandSave}
                selectedProjectId={selectedProjectId}
                busy={busy}
                topics={topics}
              />
            }
          />
          <Route
            path="topics"
            element={
              <TopicsPage
                topics={topics}
                selectedTopicId={selectedTopicId}
                onSelectTopicId={setSelectedTopicId}
                onGenerateTopics={handleGenerateTopics}
                onDeleteTopic={handleDeleteTopic}
                onGenerateContent={handleGenerateContent}
                busy={busy}
                selectedProjectId={selectedProjectId}
              />
            }
          />
          <Route
            path="contents"
            element={
              <ContentCenterPage
                tasks={contentTasks}
                selectedTaskId={selectedTaskId}
                onSelectTaskId={setSelectedTaskId}
                assets={assets}
                busy={busy}
                onReview={handleReview}
                loading={loadingProjectContext || loadingTaskDetail}
              />
            }
          />
          <Route
            path="publish"
            element={
              <PublishCenterPage
                tasks={contentTasks}
                selectedTaskId={selectedTaskId}
                onSelectTaskId={setSelectedTaskId}
                assets={assets}
                publishJobs={publishJobs}
                publishResults={publishResults}
                publishModes={publishModes}
                onPublishModeChange={handlePublishModeChange}
                assistPreviews={assistPreviews}
                assistRuns={assistRuns}
                onCreatePublishJob={handleCreatePublishJob}
                onRunPublishJob={handleRunPublishJob}
                onLoadAssistPreview={handleLoadAssistPreview}
                onRunAssistExecution={handleRunAssistExecution}
                busy={busy}
              />
            }
          />
          <Route
            path="media"
            element={
              <MediaCenterPage
                assets={assets}
                mediaAssets={mediaAssets}
                busy={busy}
                onGenerateMedia={handleGenerateMedia}
              />
            }
          />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
