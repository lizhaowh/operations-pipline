export type Project = {
  id: number;
  name: string;
  industry: string | null;
  goal: string | null;
  status: string;
  created_at: string;
  updated_at: string;
};

export type BrandProfile = {
  id: number;
  project_id: number;
  brand_name: string;
  brand_desc: string | null;
  target_audience: string | null;
  tone_of_voice: string | null;
  product_info_json: Record<string, unknown> | null;
  cta_rules_json: Record<string, unknown> | null;
  banned_words_json: string[] | null;
  competitor_accounts_json: Array<Record<string, unknown>> | null;
  extra_context: string | null;
};

export type Topic = {
  id: number;
  project_id: number;
  title: string;
  angle: string | null;
  source_type: string;
  heat_score: number;
  relevance_score: number;
  conversion_score: number;
  competition_score: number;
  final_score: number;
  reason: string | null;
  status: string;
  created_at: string;
};

export type ContentTask = {
  id: number;
  project_id: number;
  topic_id: number;
  workflow_type: string;
  status: string;
  scheduled_at: string | null;
  approved_at: string | null;
  published_at: string | null;
  created_at: string;
  updated_at: string;
};

export type ContentAsset = {
  id: number;
  task_id: number;
  platform: string;
  asset_type: string;
  title: string | null;
  outline_json: { sections?: Array<{ heading: string; points: string[] }> } | null;
  content_markdown: string | null;
  summary: string | null;
  tags_json: string[] | null;
  cover_text: string | null;
  cta_text: string | null;
  version: number;
  review_status: string;
  created_at: string;
  updated_at: string;
};

export type PublishJob = {
  id: number;
  task_id: number;
  content_asset_id: number;
  platform: string;
  publish_mode: string;
  status: string;
  scheduled_at: string | null;
  started_at: string | null;
  finished_at: string | null;
  retry_count: number;
  last_error: string | null;
  created_at: string;
  updated_at: string;
};

export type PublishResult = {
  id: number;
  publish_job_id: number;
  platform_post_id: string | null;
  post_url: string | null;
  published_at: string | null;
  raw_response_json: Record<string, unknown> | null;
  created_at: string;
};

export type PublishExecutionPreview = {
  platform: string;
  can_run: boolean;
  launch_mode: string;
  start_url: string | null;
  storage_state_path: string | null;
  selectors: Record<string, string>;
  checks: Array<{ ok: boolean; code: string; message: string }>;
  steps: string[];
  notes: string[];
  payload_summary: Record<string, unknown>;
};

export type PublishExecutionRun = {
  status: string;
  reason?: string | null;
  platform?: string | null;
  start_url?: string | null;
  next_action?: string | null;
  checks?: Array<{ ok: boolean; code: string; message: string }> | null;
  filled_fields?: Record<string, unknown> | null;
};

export type DashboardOverview = {
  project_id: number;
  project_name: string;
  topic_count: number;
  content_task_count: number;
  pending_review_count: number;
  approved_asset_count: number;
  publish_job_count: number;
  published_job_count: number;
};

export type ContentTaskDetail = {
  task: ContentTask;
  assets: ContentAsset[];
};

export type MediaAsset = {
  id: number;
  task_id: number;
  content_asset_id: number | null;
  platform: string;
  media_type: string;
  role: string;
  title: string | null;
  prompt_text: string | null;
  file_url: string | null;
  file_path: string | null;
  status: string;
  metadata_json: Record<string, unknown> | Array<unknown> | null;
  created_at: string;
  updated_at: string;
};
