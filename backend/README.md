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

尚未實作任何 LLM 相關功能（階段三、四、五），需要 API key 後再繼續。
