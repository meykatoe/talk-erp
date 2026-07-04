"""LLM 抽象層，把 Text-to-SQL 與回答生成包起來，方便之後替換供應商。"""

import json
from functools import lru_cache
from typing import NamedTuple, Protocol

from openai import OpenAI

from app.core.config import Settings, get_settings

_SQL_SYSTEM_PROMPT = """你是 ERP 系統的 Text-to-SQL 助理，只負責把「跟訂單、客戶、產品、庫存、銷售等 ERP 資料庫查詢相關」的問題轉換成 PostgreSQL SQL。

第一步，判斷問題是否屬於上述 ERP 資料查詢範疇：
- 若問題與 ERP 資料庫查詢無關（例如要求寫程式碼、閒聊、翻譯、通用知識問答、與這個資料庫無關的任何請求），把 is_relevant 設為 false，sql 留空字串，不要嘗試生成 SQL
- 只有問題確實是在問這個資料庫裡的資料時，才把 is_relevant 設為 true 並依下列規則產生 SQL

SQL 規則：
1. 只能使用下方提供的資料表與欄位，不可捏造不存在的表或欄位
2. 只能產生單一條 SELECT 敘述（可用 WITH CTE），禁止任何會修改資料的語法
3. 資料表需加上 schema 前綴（例如 sales.salesorderheader）
4. sql 欄位只放 SQL 本身，不要加上任何說明文字、markdown 或 SQL 註解
5. 每個別名只能引用「該別名對應表格實際擁有」的欄位；欄位屬於別的表格時要先 JOIN 到那張表，不可憑印象假設某別名有其他表格的欄位
6. 需要用到 CTE 以外的衍生欄位（例如分類名稱）時，該欄位必須先在 CTE 的 SELECT 中列出並往上層傳遞，不可在上層直接引用 CTE 沒有輸出的欄位

{schema}

範例（示範正確的別名與 JOIN 寫法）：
問題：各產品類別的銷售總額
SQL：SELECT pc.name AS category_name, SUM(sod.unitprice * sod.orderqty * (1 - sod.unitpricediscount)) AS total_sales FROM production.productcategory pc JOIN production.productsubcategory ps ON ps.productcategoryid = pc.productcategoryid JOIN production.product p ON p.productsubcategoryid = ps.productsubcategoryid JOIN sales.salesorderdetail sod ON sod.productid = p.productid GROUP BY pc.name ORDER BY total_sales DESC

問題：哪些客戶的訂單總金額超過 5000
SQL：SELECT so.customerid, SUM(so.totaldue) AS total_due FROM sales.salesorderheader so GROUP BY so.customerid HAVING SUM(so.totaldue) > 5000 ORDER BY total_due DESC

問題：幫我寫一段 Python 氣泡排序程式碼
（與 ERP 資料查詢無關 -> is_relevant: false, sql: ""）
"""

_ANSWER_SYSTEM_PROMPT = """你是 ERP 系統的資料助理，請根據 SQL 查詢結果，用繁體中文簡潔地回答使用者的問題。
如果查詢結果是空的，請直接說明查無資料，不要編造內容。
"""


class IrrelevantQuestionError(Exception):
    """問題與 ERP 資料查詢無關，LLM 判斷後拒絕產生 SQL。"""


class SqlGeneration(NamedTuple):
    is_relevant: bool
    sql: str


class LLMClient(Protocol):
    def generate_sql(
        self,
        question: str,
        schema_context: str,
        previous_sql: str | None = None,
        previous_error: str | None = None,
    ) -> SqlGeneration: ...

    def generate_answer(self, question: str, sql: str, rows: list[dict]) -> str: ...


class OpenAILLMClient:
    def __init__(self, settings: Settings) -> None:
        self._client = OpenAI(api_key=settings.llm_api_key)
        self._model = settings.llm_model

    def generate_sql(
        self,
        question: str,
        schema_context: str,
        previous_sql: str | None = None,
        previous_error: str | None = None,
    ) -> SqlGeneration:
        messages = [
            {
                "role": "system",
                "content": _SQL_SYSTEM_PROMPT.format(schema=schema_context),
            },
            {"role": "user", "content": question},
        ]
        if previous_sql and previous_error:
            messages.append({"role": "assistant", "content": previous_sql})
            messages.append(
                {
                    "role": "user",
                    "content": (
                        f"上面這條 SQL 執行時發生錯誤：{previous_error}\n"
                        "請修正後只回傳新的 SQL。"
                    ),
                }
            )
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "sql_query",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "is_relevant": {"type": "boolean"},
                            "sql": {"type": "string"},
                        },
                        "required": ["is_relevant", "sql"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                },
            },
            temperature=0,
            max_tokens=500,
        )
        content = response.choices[0].message.content or "{}"
        data = json.loads(content)
        return SqlGeneration(is_relevant=data["is_relevant"], sql=data["sql"])

    def generate_answer(self, question: str, sql: str, rows: list[dict]) -> str:
        payload = json.dumps(rows[:20], ensure_ascii=False, default=str)
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": _ANSWER_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"問題：{question}\nSQL：{sql}\n"
                        f"查詢結果（JSON，最多 20 筆）：{payload}"
                    ),
                },
            ],
            temperature=0.2,
            max_tokens=300,
        )
        return response.choices[0].message.content or ""


@lru_cache
def get_llm_client() -> LLMClient:
    settings = get_settings()
    if settings.llm_provider != "openai":
        raise ValueError(f"不支援的 LLM 供應商：{settings.llm_provider}")
    return OpenAILLMClient(settings)
