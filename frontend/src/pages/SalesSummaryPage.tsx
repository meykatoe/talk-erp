import { useState } from 'react';
import { fetchSalesSummary } from '../api/sales';
import { useAsync } from '../hooks/useAsync';
import { StatusBanner } from '../components/common/StatusBanner';

function currentMonth(): string {
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
}

export function SalesSummaryPage() {
  const [monthInput, setMonthInput] = useState(currentMonth());
  const [month, setMonth] = useState(currentMonth());

  const { data, loading, error } = useAsync(() => fetchSalesSummary(month), [month]);

  const maxRevenue = data ? Math.max(...data.by_category.map((c) => Number(c.revenue)), 1) : 1;

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    setMonth(monthInput);
  };

  return (
    <section>
      <h1>銷售彙總</h1>
      <form className="filter-bar" onSubmit={handleSubmit}>
        <label htmlFor="month">月份</label>
        <input id="month" type="month" value={monthInput} onChange={(event) => setMonthInput(event.target.value)} />
        <button type="submit">查詢</button>
      </form>

      <StatusBanner loading={loading} error={error} />

      {data && (
        <>
          <div className="summary-cards">
            <div className="summary-card">
              <span className="summary-label">總訂單數</span>
              <span className="summary-value">{data.total_orders.toLocaleString()}</span>
            </div>
            <div className="summary-card">
              <span className="summary-label">總營收</span>
              <span className="summary-value">${Number(data.total_revenue).toLocaleString()}</span>
            </div>
          </div>

          <h2>各產品類別營收排行</h2>
          {data.by_category.length === 0 ? (
            <p className="status status-empty">該月份無銷售紀錄</p>
          ) : (
            <div className="bar-chart">
              {data.by_category.map((category) => (
                <div className="bar-row" key={category.category}>
                  <span className="bar-label">{category.category}</span>
                  <div className="bar-track">
                    <div
                      className="bar-fill"
                      style={{ width: `${(Number(category.revenue) / maxRevenue) * 100}%` }}
                    />
                  </div>
                  <span className="bar-value">${Number(category.revenue).toLocaleString()}</span>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </section>
  );
}
