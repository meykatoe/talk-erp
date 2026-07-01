import { useState } from 'react';
import { fetchProducts } from '../api/products';
import { useAsync } from '../hooks/useAsync';
import { DataTable, type Column } from '../components/common/DataTable';
import { StatusBanner } from '../components/common/StatusBanner';
import type { Product } from '../types/product';

const PAGE_SIZE = 20;

const COLUMNS: Column<Product>[] = [
  { key: 'productid', header: '產品編號' },
  { key: 'name', header: '名稱' },
  { key: 'productnumber', header: '產品代碼' },
  {
    key: 'listprice',
    header: '牌價',
    accessor: (product) => `$${Number(product.listprice).toFixed(2)}`,
  },
];

export function ProductsPage() {
  const [page, setPage] = useState(0);
  const { data, loading, error } = useAsync(
    () => fetchProducts({ skip: page * PAGE_SIZE, limit: PAGE_SIZE }),
    [page],
  );

  return (
    <section>
      <h1>產品清單</h1>
      <StatusBanner loading={loading} error={error} empty={data?.length === 0} />
      {data && data.length > 0 && <DataTable columns={COLUMNS} rows={data} rowKey={(row) => row.productid} />}
      <div className="pagination">
        <button type="button" onClick={() => setPage((p) => Math.max(0, p - 1))} disabled={page === 0}>
          上一頁
        </button>
        <span>第 {page + 1} 頁</span>
        <button
          type="button"
          onClick={() => setPage((p) => p + 1)}
          disabled={!data || data.length < PAGE_SIZE}
        >
          下一頁
        </button>
      </div>
    </section>
  );
}
