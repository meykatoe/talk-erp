# TalkERP Frontend

React + TypeScript + Vite。對接 `backend` 目前已提供的查詢端點（產品、訂單、庫存、銷售彙總），
並預留「智能查詢」頁面骨架，待後端階段三～五（LLM / RAG）完成後再串接。

## 開發環境設定

```bash
cd frontend
npm install
cp .env.example .env  # 依實際後端位址調整 VITE_API_BASE_URL
npm run dev
```

- 開發伺服器：http://localhost:5173
- 後端需先啟動（見 `backend/README.md`），預設對接 `http://127.0.0.1:8000/api/v1`

## 指令

| 指令 | 說明 |
| --- | --- |
| `npm run dev` | 啟動開發伺服器（含 HMR） |
| `npm run build` | TypeScript 型別檢查 + 打包 |
| `npm run lint` | oxlint 靜態檢查 |
| `npm run preview` | 預覽打包後結果 |

## 目錄結構

```
src/
  api/         # 後端 API 呼叫，一個資源一個檔案
  types/       # 對應後端 Pydantic schema 的 TS 型別
  hooks/       # 共用邏輯（useAsync：GET 請求的 loading/error 樣板）
  components/
    layout/    # AppLayout、NavBar
    common/    # DataTable、StatusBanner 等可重用元件
  pages/       # 依路由拆分的頁面
  App.tsx      # 路由設定
  main.tsx     # 進入點
```

## 頁面對應

| 路由 | 對應後端端點 | 說明 |
| --- | --- | --- |
| `/products` | `GET /products` | 產品清單（分頁） |
| `/orders` | `GET /orders?customer_id=` | 訂單查詢，可依客戶編號篩選 |
| `/inventory` | `GET /inventory/low-stock` | 低庫存清單 |
| `/sales` | `GET /sales/summary?month=` | 銷售彙總（總計卡片 + 類別營收長條圖） |
| `/query` | 尚未串接 | 智能查詢介面骨架，需 LLM API key 後於階段五串接 |
