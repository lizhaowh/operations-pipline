import type { FormEvent } from "react";
import { useMemo, useState } from "react";

import { EmptyState, StatusBadge } from "../components/ui";
import type { BrandFormState } from "../types-extra";
import type { BrandProfile, Topic } from "../types";

function hasStrategyRecord(brandForm: BrandFormState) {
  return [
    brandForm.brand_name,
    brandForm.brand_desc,
    brandForm.target_audience,
    brandForm.tone_of_voice,
    brandForm.product_info_text,
    brandForm.cta_rules_text,
    brandForm.banned_words_text,
    brandForm.competitor_accounts_text,
    brandForm.extra_context,
  ].some((item) => item.trim() !== "");
}

export function StrategyPage({
  brandProfile,
  brandForm,
  onBrandFormChange,
  onBrandSave,
  selectedProjectId,
  busy,
  topics,
}: {
  brandProfile: BrandProfile | null;
  brandForm: BrandFormState;
  onBrandFormChange: (key: keyof BrandFormState, value: string) => void;
  onBrandSave: (event: FormEvent) => Promise<void>;
  selectedProjectId: number | null;
  busy: string | null;
  topics: Topic[];
}) {
  const [openEditor, setOpenEditor] = useState(false);
  const exists = useMemo(() => brandProfile != null, [brandProfile]);

  async function handleSubmit(event: FormEvent) {
    await onBrandSave(event);
    if (busy !== "brand") {
      setOpenEditor(false);
    }
  }

  return (
    <div className="project-page">
      <div className="table-page-shell">
        <div className="table-page-toolbar">
          <div className="table-page-title">
            <div className="page-breadcrumb">内容管理 / 品牌策略</div>
            <h1>品牌策略</h1>
          </div>
        </div>

        {selectedProjectId == null ? (
          <div className="table-empty-wrap">
            <EmptyState text="请先在项目管理中选择项目。" />
          </div>
        ) : (
          <div className="table-shell table-shell-strong">
            <div className="table-toolbar">
              <div className="table-toolbar-left">
                <span className="table-toolbar-title">策略列表</span>
              </div>
              <div className="table-toolbar-right">
                <button className="table-text-button" onClick={() => setOpenEditor(true)}>
                  {exists ? "新建策略" : "新建策略"}
                </button>
              </div>
            </div>

            {!exists ? (
              <div className="table-empty-wrap">
                <EmptyState text="暂无品牌策略，请点击右上角新建策略。" />
              </div>
            ) : (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>品牌名称</th>
                    <th>内容语气</th>
                    <th>目标用户</th>
                    <th>选题数</th>
                    <th>状态</th>
                    <th>操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>{brandProfile?.brand_name || "未填写"}</td>
                    <td>{brandProfile?.tone_of_voice || "未填写"}</td>
                    <td className="table-goal-cell">{brandProfile?.target_audience || "未填写"}</td>
                    <td>{topics.length}</td>
                    <td>
                      <StatusBadge value="approved" />
                    </td>
                    <td>
                      <div className="table-action-row">
                        <button className="table-text-button" onClick={() => setOpenEditor(true)}>
                          编辑
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            )}
          </div>
        )}
      </div>

      {openEditor ? (
        <div className="modal-backdrop" onClick={() => setOpenEditor(false)}>
          <div className="modal-card" onClick={(event) => event.stopPropagation()}>
            <div className="modal-head">
              <div>
                <h3>{exists ? "编辑品牌策略" : "新建品牌策略"}</h3>
              </div>
              <button className="modal-close" onClick={() => setOpenEditor(false)}>
                关闭
              </button>
            </div>

            <form className="form-grid" onSubmit={(event) => void handleSubmit(event)}>
              <div className="two-column-grid">
                <label className="field-block" htmlFor="brand-name">
                  <span>品牌名称</span>
                  <input
                    id="brand-name"
                    className="app-input"
                    value={brandForm.brand_name}
                    onChange={(event) => onBrandFormChange("brand_name", event.target.value)}
                  />
                </label>
                <label className="field-block" htmlFor="brand-tone">
                  <span>内容语气</span>
                  <input
                    id="brand-tone"
                    className="app-input"
                    value={brandForm.tone_of_voice}
                    onChange={(event) => onBrandFormChange("tone_of_voice", event.target.value)}
                  />
                </label>
              </div>

              <label className="field-block" htmlFor="brand-desc">
                <span>品牌介绍</span>
                <textarea
                  id="brand-desc"
                  className="app-textarea"
                  value={brandForm.brand_desc}
                  onChange={(event) => onBrandFormChange("brand_desc", event.target.value)}
                />
              </label>

              <label className="field-block" htmlFor="audience">
                <span>目标用户</span>
                <textarea
                  id="audience"
                  className="app-textarea"
                  value={brandForm.target_audience}
                  onChange={(event) => onBrandFormChange("target_audience", event.target.value)}
                />
              </label>

              <label className="field-block" htmlFor="product-info">
                <span>产品信息 JSON</span>
                <textarea
                  id="product-info"
                  className="app-textarea"
                  value={brandForm.product_info_text}
                  onChange={(event) => onBrandFormChange("product_info_text", event.target.value)}
                />
              </label>

              <label className="field-block" htmlFor="competitors">
                <span>竞品账号 JSON 数组</span>
                <textarea
                  id="competitors"
                  className="app-textarea"
                  value={brandForm.competitor_accounts_text}
                  onChange={(event) =>
                    onBrandFormChange("competitor_accounts_text", event.target.value)
                  }
                />
              </label>

              <label className="field-block" htmlFor="extra-context">
                <span>额外上下文</span>
                <textarea
                  id="extra-context"
                  className="app-textarea"
                  value={brandForm.extra_context}
                  onChange={(event) => onBrandFormChange("extra_context", event.target.value)}
                />
              </label>

              <div className="modal-actions">
                <button type="button" className="secondary-button" onClick={() => setOpenEditor(false)}>
                  取消
                </button>
                <button
                  className="primary-button"
                  disabled={busy === "brand" || !brandForm.brand_name.trim()}
                >
                  {busy === "brand" ? "保存中..." : "保存"}
                </button>
              </div>
            </form>
          </div>
        </div>
      ) : null}
    </div>
  );
}
