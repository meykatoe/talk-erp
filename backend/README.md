# TalkERP Backend

階段一骨架：FastAPI + SQLAlchemy，對接已匯入的 `talkerp`（AdventureWorks）資料庫。

## 開發環境設定

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # 填入實際的 DB 密碼
```

## 啟動

```bash
uvicorn app.main:app --reload
```

- API 文件：http://127.0.0.1:8000/docs
- 健康檢查：`GET /api/v1/health`、`GET /api/v1/health/db`

## 查詢端點

| 端點 | 說明 |
| --- | --- |
| `GET /api/v1/products` | 產品清單（`skip`、`limit` 分頁） |
| `GET /api/v1/orders?customer_id=xxx` | 訂單清單，可選依客戶篩選 |
| `GET /api/v1/inventory/low-stock` | 依產品彙總各倉庫庫存量，列出總量低於 `reorderpoint` 的品項 |
| `GET /api/v1/sales/summary?month=YYYY-MM` | 該月總訂單數、總營收，並依產品類別列出營收排行 |
| `POST /api/v1/query/structured` | Text-to-SQL：自然語言問題 → LLM 產生 SQL → 唯讀執行 → LLM 生成回答 |

## Text-to-SQL（階段三）

`POST /api/v1/query/structured`，body：`{"question": "2022年7月哪個產品類別銷售額最高"}`

流程：
1. LLM（`LLM_MODEL`，預設 `gpt-4o-mini`）依 `app/core/schema_context.py` 的白名單 schema 產生 SQL（structured output 限制只回傳 `{"sql": "..."}`），system prompt 附帶別名/JOIN 規則與 2 組 few-shot 範例，降低幻覈欄位或搞混別名的機率
2. `app/core/sql_guard.py` 檢查：只允許單一條 `SELECT`/`WITH`、禁止修改語法與 SQL 註解、未帶 `LIMIT` 時自動補 `LIMIT 200`，並用 `find_unknown_tables` 靜態比對 `FROM`/`JOIN` 是否都在白名單內（不用等資料庫報錯）
3. 用唯讀帳號 `talkerp_readonly`（`POSTGRES_READONLY_USER`）執行查詢，該帳號僅有 `person`/`production`/`sales` schema 的 `SELECT` 權限，並在角色層設定 `statement_timeout=5s`、`default_transaction_read_only=on`，即使檢查有漏洞資料庫也擋得住
4. SQL 引用未知資料表或執行失敗時，會把原因回饋給 LLM 重新產生一次 SQL（最多 2 次嘗試）
5. 查詢結果（最多取前 20 筆）連同問題丟回 LLM，生成繁體中文的自然語言回答；兩次 LLM 呼叫都設了 `max_tokens` 上限（SQL 500、回答 300）控制成本

若要重建 `talkerp_readonly` 角色：

```sql
CREATE ROLE talkerp_readonly LOGIN PASSWORD '...';
GRANT CONNECT ON DATABASE talkerp TO talkerp_readonly;
GRANT USAGE ON SCHEMA person, production, sales TO talkerp_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA person, production, sales TO talkerp_readonly;
ALTER ROLE talkerp_readonly SET statement_timeout = '5s';
ALTER ROLE talkerp_readonly SET default_transaction_read_only = on;
```

## 日誌 Log

- 全部請求會經 `RequestLoggingMiddleware` 記錄 method、path、status、耗時與 `request_id`（同步放進回應標頭 `X-Request-ID`，方便對照前端錯誤回報）。
- `logs/app.log`：所有等級（依 `LOG_LEVEL` 設定），每日午夜輪替，保留 30 天。
- `logs/error.log`：僅 ERROR 以上，未處理例外會附完整 traceback，方便快速定位 bug。
- 主控台同步輸出，`--reload` 開發時可即時看到。
- 可於 `.env` 調整 `LOG_LEVEL`（預設 `INFO`）與 `LOG_DIR`（預設 `logs`）。
- 即時查看：`tail -f logs/app.log` 或只看錯誤 `tail -f logs/error.log`。

## 目錄結構

```
app/
  core/       # 設定與資料庫連線
  models/     # SQLAlchemy models（對應 talkerp 既有資料表，不建立新表）
  schemas/    # Pydantic 回傳格式
  api/v1/     # 路由
```

## 目前涵蓋的資料表

| 領域 | Schema.Table |
| --- | --- |
| 客戶 | person.businessentity, person.person, sales.customer, sales.store |
| 產品 | production.productcategory, production.productsubcategory, production.product |
| 庫存 | production.location, production.productinventory |
| 訂單 | sales.salesorderheader, sales.salesorderdetail |

階段三 Text-to-SQL 已完成，階段四（RAG 文件問答）、階段五（意圖路由）尚未實作。
