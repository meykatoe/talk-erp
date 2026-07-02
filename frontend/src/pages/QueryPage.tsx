import { useState } from 'react';
import { postStructuredQuery } from '../api/query';
import { DataTable } from '../components/common/DataTable';

interface ChatMessage {
  role: 'user' | 'assistant';
  text: string;
  routeLabel?: '結構化查詢' | '文件檢索' | '錯誤';
  sql?: string;
  columns?: string[];
  rows?: Record<string, unknown>[];
}

export function QueryPage() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const question = input.trim();
    if (!question || loading) return;

    setMessages((prev) => [...prev, { role: 'user', text: question }]);
    setInput('');
    setLoading(true);

    try {
      const result = await postStructuredQuery(question);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: result.answer,
          routeLabel: '結構化查詢',
          sql: result.sql,
          columns: result.columns,
          rows: result.rows,
        },
      ]);
    } catch (error) {
      const message = error instanceof Error ? error.message : '未知錯誤';
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', text: `查詢失敗：${message}`, routeLabel: '錯誤' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section>
      <h1>智能查詢</h1>
      <p className="page-hint">
        自然語言問答入口：目前僅支援結構化查詢（Text-to-SQL），文件檢索（RAG）與意圖路由尚未實作。
      </p>

      <div className="chat-window">
        {messages.length === 0 && <p className="status status-empty">輸入問題開始對話</p>}
        {messages.map((message, index) => (
          <div key={index} className={`chat-message chat-message-${message.role}`}>
            {message.routeLabel && <span className="badge badge-info">{message.routeLabel}</span>}
            <p>{message.text}</p>
            {message.sql && (
              <details className="query-sql">
                <summary>查看產生的 SQL</summary>
                <pre>{message.sql}</pre>
              </details>
            )}
            {message.rows && message.rows.length > 0 && message.columns && (
              <DataTable
                columns={message.columns.map((col) => ({ key: col, header: col }))}
                rows={message.rows.map((row, rowIndex) => ({ ...row, __rowKey: rowIndex }))}
                rowKey={(row) => row.__rowKey as number}
              />
            )}
          </div>
        ))}
        {loading && <p className="status status-loading">查詢中…</p>}
      </div>

      <form className="chat-input-bar" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="例如：2022年7月哪個產品類別銷售額最高？"
          value={input}
          onChange={(event) => setInput(event.target.value)}
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          送出
        </button>
      </form>
    </section>
  );
}
