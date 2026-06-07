import { formatDateTime } from "../helpers";
import { EmptyState, PlatformBadge, StatusBadge } from "../components/ui";
import type { ContentAsset, MediaAsset } from "../types";

export function MediaCenterPage({
  assets,
  mediaAssets,
  busy,
  onGenerateMedia,
}: {
  assets: ContentAsset[];
  mediaAssets: MediaAsset[];
  busy: string | null;
  onGenerateMedia: (contentAssetId: number) => Promise<void>;
}) {
  return (
    <div className="project-page">
      <div className="table-page-shell">
        <div className="table-page-toolbar">
          <div className="table-page-title">
            <div className="page-breadcrumb">内容管理 / 素材中心</div>
            <h1>素材中心</h1>
          </div>
        </div>

        <div className="table-shell table-shell-strong">
          <div className="table-toolbar">
            <div className="table-toolbar-left">
              <span className="table-toolbar-title">素材列表</span>
            </div>
          </div>

          {assets.length === 0 ? (
            <div className="table-empty-wrap">
              <EmptyState text="请先在内容工单中选择任务。" />
            </div>
          ) : (
            <table className="data-table">
              <thead>
                <tr>
                  <th>平台</th>
                  <th>内容标题</th>
                  <th>素材数量</th>
                  <th>最新更新时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {assets.map((asset) => {
                  const count = mediaAssets.filter((item) => item.content_asset_id === asset.id).length;
                  const latest = mediaAssets
                    .filter((item) => item.content_asset_id === asset.id)
                    .sort((a, b) => b.updated_at.localeCompare(a.updated_at))[0];

                  return (
                    <tr key={asset.id}>
                      <td>
                        <PlatformBadge value={asset.platform} />
                      </td>
                      <td>{asset.title ?? "未命名"}</td>
                      <td>{count}</td>
                      <td>{latest ? formatDateTime(latest.updated_at) : "未生成"}</td>
                      <td>
                        <div className="table-action-row">
                          <button
                            className="table-text-button"
                            onClick={() => void onGenerateMedia(asset.id)}
                            disabled={busy === `media-${asset.id}`}
                          >
                            {busy === `media-${asset.id}` ? "生成中..." : "生成素材"}
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </div>

        {mediaAssets.length > 0 ? (
          <div className="table-shell table-shell-strong">
            <div className="table-toolbar">
              <div className="table-toolbar-left">
                <span className="table-toolbar-title">素材预览</span>
              </div>
            </div>
            <div className="media-grid media-grid-padded">
              {mediaAssets.map((item) => (
                <article className="media-card" key={item.id}>
                  {item.file_url ? (
                    <img className="media-preview" src={item.file_url} alt={item.title ?? "媒体预览"} />
                  ) : (
                    <div className="media-placeholder">暂无预览</div>
                  )}
                  <div className="media-body">
                    <div className="list-item-head">
                      <strong>{item.title ?? "未命名素材"}</strong>
                      <StatusBadge value={item.status} />
                    </div>
                    <div className="badge-row">
                      <PlatformBadge value={item.platform} />
                      <span className="chip">{item.role}</span>
                      <span className="chip">{formatDateTime(item.updated_at)}</span>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
