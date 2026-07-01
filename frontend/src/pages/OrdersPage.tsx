import { useState } from 'react';
import { fetchOrders } from '../api/orders';
import { useAsync } from '../hooks/useAsync';
import { DataTable, type Column } from '../components/common/DataTable';
import { StatusBanner } from '../components/common/StatusBanner';
import type { Order } from '../types/order';

const PAGE_SIZE = 20;

const COLUMNS: Column<Order>[] = [
  { key: 'salesorderid', header: '訂單編號' },
  { key: 'customerid', header: '客戶編號' },
  { key: 'orderdate', header: '下單日', accessor: (order) => order.orderdate.slice(0, 10) },
  { key: 'shipdate', header: '出貨日', accessor: (order) => order.shipdate?.slice(0, 10) ?? '未出貨' },
  { key: 'status', header: '狀態' },
  {
    key: 'totaldue',
    header: '應付總額',
    accessor: (order) => (order.totaldue ? `$${Number(order.totaldue).toFixed(2)}` : '—'),
  },
];

export function OrdersPage() {
  const [customerIdInput, setCustomerIdInput] = useState('');
  const [customerId, setCustomerId] = useState<number | undefined>(undefined);
  const [page, setPage] = useState(0);

  const { data, loading, error } = useAsync(
    () => fetchOrders({ customerId, skip: page * PAGE_SIZE, limit: PAGE_SIZE }),
    [customerId, page],
  );

  const handleSearch = (event: React.FormEvent) => {
    event.preventDefault();
    setPage(0);
    setCustomerId(customerIdInput ? Number(customerIdInput) : undefined);
  };

  return (
    <section>
      <h1>訂單查詢</h1>
      <form className="filter-bar" onSubmit={handleSearch}>
        <label htmlFor="customer-id">客戶編號</label>
        <input
          id="customer-id"
          type="number"
          placeholder="留空查詢全部"
          value={customerIdInput}
          onChange={(event) => setCustomerIdInput(event.target.value)}
        />
        <button type="submit">查詢</button>
      </form>

      <StatusBanner loading={loading} error={error} empty={data?.length === 0} />
      {data && data.length > 0 && <DataTable columns={COLUMNS} rows={data} rowKey={(row) => row.salesorderid} />}
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
