import type {
  BrandProfile,
  ContentAsset,
  PublishExecutionRun,
  PublishExecutionPreview,
  ContentTaskDetail,
  ContentTask,
  DashboardOverview,
  MediaAsset,
  Project,
  PublishJob,
  PublishResult,
  Topic,
} from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed: ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export const api = {
  listProjects: () => request<Project[]>("/projects"),
  createProject: (payload: { name: string; industry?: string; goal?: string }) =>
    request<Project>("/projects", { method: "POST", body: JSON.stringify(payload) }),
  updateProject: (projectId: number, payload: { name: string; industry?: string; goal?: string }) =>
    request<Project>(`/projects/${projectId}`, { method: "PUT", body: JSON.stringify(payload) }),
  deleteProject: (projectId: number) =>
    request<void>(`/projects/${projectId}`, { method: "DELETE" }),
  getDashboard: (projectId: number) => request<DashboardOverview>(`/dashboard/projects/${projectId}`),
  getBrandProfile: (projectId: number) => request<BrandProfile>(`/brand-profiles/projects/${projectId}`),
  upsertBrandProfile: (payload: Omit<BrandProfile, "id">) =>
    request<BrandProfile>("/brand-profiles", { method: "POST", body: JSON.stringify(payload) }),
  listTopics: (projectId: number) => request<Topic[]>(`/topics/projects/${projectId}`),
  generateTopics: (projectId: number) =>
    request<{ message: string; project_id: number; count: number }>(`/topics/projects/${projectId}/generate`, {
      method: "POST",
    }),
  deleteTopic: (projectId: number, topicId: number) =>
    request<void>(`/topics/projects/${projectId}/${topicId}`, { method: "DELETE" }),
  generateContent: (payload: { topic_id: number; platforms: string[] }) =>
    request<ContentTask>("/contents/generate", { method: "POST", body: JSON.stringify(payload) }),
  listContentTasks: (projectId: number) => request<ContentTask[]>(`/contents/projects/${projectId}/tasks`),
  getContentTask: (taskId: number) => request<ContentTask>(`/contents/tasks/${taskId}`),
  getContentTaskDetail: (taskId: number) => request<ContentTaskDetail>(`/contents/tasks/${taskId}/detail`),
  listContentAssets: (taskId: number) => request<ContentAsset[]>(`/contents/tasks/${taskId}/assets`),
  listMediaByProject: (projectId: number) => request<MediaAsset[]>(`/media/projects/${projectId}`),
  listMediaByTask: (taskId: number) => request<MediaAsset[]>(`/media/tasks/${taskId}`),
  generateMediaForAsset: (contentAssetId: number, payload?: { roles?: string[] }) =>
    request<MediaAsset[]>(`/media/content-assets/${contentAssetId}/generate`, {
      method: "POST",
      body: JSON.stringify(payload ?? { roles: ["cover", "body"] }),
    }),
  reviewAsset: (assetId: number, payload: { approved: boolean; notes?: string }) =>
    request<ContentAsset>(`/review/assets/${assetId}`, { method: "POST", body: JSON.stringify(payload) }),
  createPublishJob: (payload: { content_asset_id: number; publish_mode: string; scheduled_at?: string | null }) =>
    request<PublishJob>("/publish/jobs", { method: "POST", body: JSON.stringify(payload) }),
  getAssistPreview: (assetId: number) => request<PublishExecutionPreview>(`/publish/assets/${assetId}/assist-preview`),
  runAssistExecution: (assetId: number) =>
    request<PublishExecutionRun>(`/publish/assets/${assetId}/assist-run`, { method: "POST" }),
  runPublishJob: (jobId: number) => request<PublishResult>(`/publish/jobs/${jobId}/run`, { method: "POST" }),
  getPublishJob: (jobId: number) => request<PublishJob>(`/publish/jobs/${jobId}`),
};
