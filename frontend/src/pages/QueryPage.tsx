import { useState } from 'react';

interface ChatMessage {
  role: 'user' | 'assistant';
  text: string;
  routeLabel?: '結構化查詢' | '文件檢索' | '尚未啟用';
}

const NOT_READY_MESSAGE =
  '智能查詢功能仰賴 LLM API，目前專案尚未設定 API Key，此頁面為介面骨架，待階段三～五完成後即可串接。';

export function QueryPage() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (!input.trim()) return;

    setMessages((prev) => [
      ...prev,
      { role: 'user', text: input },
      { role: 'assistant', text: NOT_READY_MESSAGE, routeLabel: '尚未啟用' },
    ]);
    setInput('');
  };

  return (
    <section>
      <h1>智能查詢</h1>
      <p className="page-hint">
        自然語言問答入口：未來會依問題內容自動判斷走「結構化查詢」（Text-to-SQL）或「文件檢索」（RAG）。
      </p>

      <div className="chat-window">
        {messages.length === 0 && <p className="status status-empty">輸入問題開始對話</p>}
        {messages.map((message, index) => (
          <div key={index} className={`chat-message chat-message-${message.role}`}>
            {message.routeLabel && <span className="badge badge-info">{message.routeLabel}</span>}
            <p>{message.text}</p>
          </div>
        ))}
      </div>

      <form className="chat-input-bar" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="例如：上個月哪個產品類別銷售額最高？"
          value={input}
          onChange={(event) => setInput(event.target.value)}
        />
        <button type="submit">送出</button>
      </form>
    </section>
  );
}
