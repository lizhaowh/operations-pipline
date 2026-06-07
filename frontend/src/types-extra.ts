import type { ContentTask, DashboardOverview, Project, Topic } from "./types";

export type Notice = { type: "success" | "error"; text: string } | null;

export type BrandFormState = {
  brand_name: string;
  brand_desc: string;
  target_audience: string;
  tone_of_voice: string;
  product_info_text: string;
  cta_rules_text: string;
  banned_words_text: string;
  competitor_accounts_text: string;
  extra_context: string;
};

export type { ContentTask, DashboardOverview, Project, Topic };

