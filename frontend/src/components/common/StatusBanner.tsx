interface StatusBannerProps {
  loading: boolean;
  error: string | null;
  empty?: boolean;
  emptyText?: string;
}

export function StatusBanner({ loading, error, empty, emptyText = '目前沒有資料' }: StatusBannerProps) {
  if (loading) return <p className="status status-loading">載入中…</p>;
  if (error) return <p className="status status-error">發生錯誤：{error}</p>;
  if (empty) return <p className="status status-empty">{emptyText}</p>;
  return null;
}
