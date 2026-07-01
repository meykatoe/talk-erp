import { fetchLowStock } from '../api/inventory';
import { useAsync } from '../hooks/useAsync';
import { DataTable, type Column } from '../components/common/DataTable';
import { StatusBanner } from '../components/common/StatusBanner';
import type { LowStockItem } from '../types/inventory';

const COLUMNS: Column<LowStockItem>[] = [
  { key: 'productid', header: '產品編號' },
  { key: 'name', header: '名稱' },
  { key: 'productnumber', header: '產品代碼' },
  { key: 'total_quantity', header: '目前總庫存' },
  { key: 'reorderpoint', header: '再訂購點' },
  {
    key: 'status',
    header: '狀態',
    accessor: (item) => (
      <span className={item.total_quantity === 0 ? 'badge badge-danger' : 'badge badge-warning'}>
        {item.total_quantity === 0 ? '缺貨' : '偏低'}
      </span>
    ),
  },
];

export function InventoryPage() {
  const { data, loading, error } = useAsync(() => fetchLowStock({ limit: 50 }), []);

  return (
    <section>
      <h1>低庫存清單</h1>
      <p className="page-hint">依產品彙總各倉位庫存量，列出總量低於再訂購點（ReorderPoint）的品項。</p>
      <StatusBanner loading={loading} error={error} empty={data?.length === 0} emptyText="目前沒有低庫存品項" />
      {data && data.length > 0 && <DataTable columns={COLUMNS} rows={data} rowKey={(row) => row.productid} />}
    </section>
  );
}
