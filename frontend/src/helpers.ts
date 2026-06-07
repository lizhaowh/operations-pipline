import type { BrandProfile } from "./types";

export function parseJsonText(value: string): Record<string, unknown> | null {
  const trimmed = value.trim();
  if (!trimmed) return null;
  return JSON.parse(trimmed) as Record<string, unknown>;
}

export function parseJsonArrayText(value: string): Array<Record<string, unknown>> | null {
  const trimmed = value.trim();
  if (!trimmed) return null;
  return JSON.parse(trimmed) as Array<Record<string, unknown>>;
}

export function parseLines(value: string): string[] | null {
  const items = value
    .split("\n")
    .map((item) => item.trim())
    .filter(Boolean);
  return items.length > 0 ? items : null;
}

export function fromBrandProfile(profile: BrandProfile) {
  return {
    brand_name: profile.brand_name,
    brand_desc: profile.brand_desc ?? "",
    target_audience: profile.target_audience ?? "",
    tone_of_voice: profile.tone_of_voice ?? "",
    product_info_text: profile.product_info_json
      ? JSON.stringify(profile.product_info_json, null, 2)
      : "",
    cta_rules_text: profile.cta_rules_json ? JSON.stringify(profile.cta_rules_json, null, 2) : "",
    banned_words_text: profile.banned_words_json?.join("\n") ?? "",
    competitor_accounts_text: profile.competitor_accounts_json
      ? JSON.stringify(profile.competitor_accounts_json, null, 2)
      : "",
    extra_context: profile.extra_context ?? "",
  };
}

export function getErrorMessage(error: unknown) {
  if (error instanceof Error) return error.message;
  return "发生未知错误";
}

export function formatPlatformLabel(platform: string) {
  const mapping: Record<string, string> = {
    wechat: "公众号",
    xiaohongshu: "小红书",
  };
  return mapping[platform] ?? platform;
}

export function formatStatusLabel(status: string) {
  const mapping: Record<string, string> = {
    new: "待处理",
    approved: "已通过",
    discarded: "已废弃",
    in_production: "生产中",
    draft_requested: "待生成",
    outline_generated: "已出大纲",
    article_generated: "已出正文",
    rewritten: "已改写",
    pending_review: "待审核",
    rejected: "已驳回",
    publish_pending: "待发布",
    published: "已发布",
    analyzed: "已复盘",
    scheduled: "已排期",
    running: "执行中",
    success: "已完成",
    failed: "失败",
  };
  return mapping[status] ?? status;
}

export function formatPublishModeLabel(mode: string) {
  const mapping: Record<string, string> = {
    manual_export: "人工导出",
    assisted_publish: "辅助发布",
  };
  return mapping[mode] ?? mode;
}

export function formatWorkflowLabel(workflowType: string) {
  const mapping: Record<string, string> = {
    content_generation: "内容生产",
    topic_generation: "选题生成",
    publish_workflow: "发布流程",
  };
  return mapping[workflowType] ?? workflowType;
}

export function formatTopicSourceLabel(sourceType: string) {
  const mapping: Record<string, string> = {
    llm_generated: "LLM",
    seed_template: "模板兜底",
  };
  return mapping[sourceType] ?? sourceType;
}

export function formatDateTime(value: string | null | undefined) {
  if (!value) return "未记录";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat("zh-CN", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}
