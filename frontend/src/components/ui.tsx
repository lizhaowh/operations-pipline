import type { ReactNode } from "react";

import { formatPlatformLabel, formatPublishModeLabel, formatStatusLabel } from "../helpers";

export function Panel({
  title,
  subtitle,
  actions,
  children,
}: {
  title: string;
  subtitle?: string;
  actions?: ReactNode;
  children: ReactNode;
}) {
  return (
    <section className="panel">
      <div className="panel-head">
        <div>
          <h3>{title}</h3>
          {subtitle ? <p>{subtitle}</p> : null}
        </div>
        {actions}
      </div>
      {children}
    </section>
  );
}

export function SectionHeader({
  title,
  description,
  actions,
}: {
  title: string;
  description?: string;
  actions?: ReactNode;
}) {
  return (
    <header className="section-header">
      <div>
        <h1>{title}</h1>
        {description ? <p>{description}</p> : null}
      </div>
      {actions ? <div className="section-actions">{actions}</div> : null}
    </header>
  );
}

export function StatCard({
  label,
  value,
  hint,
}: {
  label: string;
  value: string;
  hint?: string;
}) {
  return (
    <article className="stat-card">
      <span>{label}</span>
      <strong>{value}</strong>
      {hint ? <small>{hint}</small> : null}
    </article>
  );
}

export function EmptyState({ text }: { text: string }) {
  return <div className="empty-state">{text}</div>;
}

export function NoticeBanner({
  type,
  text,
}: {
  type: "success" | "error";
  text: string;
}) {
  return <div className={`notice-banner ${type}`}>{text}</div>;
}

export function StatusBadge({ value }: { value: string }) {
  return (
    <span className={`status-badge ${value}`}>
      {formatStatusLabel(value)}
    </span>
  );
}

export function PlatformBadge({ value }: { value: string }) {
  return <span className="platform-badge">{formatPlatformLabel(value)}</span>;
}

export function PublishModeBadge({ value }: { value: string }) {
  return <span className="mode-badge">{formatPublishModeLabel(value)}</span>;
}
