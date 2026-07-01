# TalkERP

ERP 混合式 AI 查詢系統 —— 以 AdventureWorks（PostgreSQL 版）作為 ERP 資料骨架，
結合 Text-to-SQL（結構化查詢）與 RAG（文件檢索）兩種路徑，示範「依資料型態選擇對應技術」的判斷力。

## 技術棧

| 分類 | 選用 |
| --- | --- |
| 資料庫 | PostgreSQL 15+（含 pgvector，供後續向量檢索用） |
| 後端 | Python + FastAPI + SQLAlchemy 2.0 |
| 前端 | React + TypeScript + Vite |
| LLM | OpenAI API（透過抽象層封裝，方便替換其他家） |
| Embedding | text-embedding-3-small |

## 目錄結構

```
backend/       FastAPI 後端（見 backend/README.md）
frontend/      React 前端（見 frontend/README.md）
documents/     規格文件、合成語料（gitignore，不進版控）
```

## 開發階段

- [x] 階段一：資料層與基礎查詢 API（不需 LLM key）
- [x] 階段二：合成文件語料（見 `documents/corpus/README.md`）
- [ ] 階段三：Text-to-SQL 查詢層（需 LLM key）
- [ ] 階段四：RAG 文件問答層（需 LLM key）
- [ ] 階段五：意圖路由整合（需 LLM key）
- [x] 階段六：前端基本功能（產品／訂單／庫存／銷售彙總頁面已完成；智能查詢頁面為骨架，待階段五串接）

## 資料庫：AdventureWorks

微軟官方的免費資料庫，已由其他用戶轉換為 PostgreSQL 版並開源。

```bash
git clone https://github.com/lorint/AdventureWorks-for-Postgres.git
```

1. 下載並解壓官方 CSV 資料，安裝 Ruby 執行 `update_csvs.rb` 轉換格式
2. 建立 `talkerp` 資料庫，執行 `install.sql` 建好 68 個資料表、5 個 schema
3. 目前後端只挑選訂單、庫存、客戶、產品相關的 11 張核心表（見 `backend/README.md`）

## 快速開始

後端啟動方式與環境設定請見 [`backend/README.md`](backend/README.md)；
前端啟動方式請見 [`frontend/README.md`](frontend/README.md)。
