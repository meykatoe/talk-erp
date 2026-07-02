"""LLM 抽象層，把 Text-to-SQL 與回答生成包起來，方便之後替換供應商。"""

import json
from functools import lru_cache
from typing import Protocol

from openai import OpenAI

from app.core.config import Settings, get_settings

_SQL_SYSTEM_PROMPT = """你是 PostgreSQL 專家，負責把使用者的自然語言問題轉換成一句 SQL 查詢。

規則：
1. 只能使用下方提供的資料表與欄位，不可捏造不存在的表或欄位
2. 只能產生單一條 SELECT 敘述（可用 WITH CTE），禁止任何會修改資料的語法
3. 資料表需加上 schema 前綴（例如 sales.salesorderheader）
4. 只回傳 SQL 本身，不要加上任何說明文字、markdown 或 SQL 註解

{schema}
"""

_ANSWER_SYSTEM_PROMPT = """你是 ERP 系統的資料助理，請根據 SQL 查詢結果，用繁體中文簡潔地回答使用者的問題。
如果查詢結果是空的，請直接說明查無資料，不要編造內容。
"""


class LLMClient(Protocol):
    def generate_sql(
        self,
        question: str,
        schema_context: str,
        previous_sql: str | None = None,
        previous_error: str | None = None,
    ) -> str: ...

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
    ) -> str:
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
                        "properties": {"sql": {"type": "string"}},
                        "required": ["sql"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                },
            },
            temperature=0,
        )
        content = response.choices[0].message.content or "{}"
        return json.loads(content)["sql"]

    def generate_answer(self, question: str, sql: str, rows: list[dict]) -> str:
        payload = json.dumps(rows[:50], ensure_ascii=False, default=str)
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": _ANSWER_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"問題：{question}\nSQL：{sql}\n"
                        f"查詢結果（JSON，最多 50 筆）：{payload}"
                    ),
                },
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content or ""


@lru_cache
def get_llm_client() -> LLMClient:
    settings = get_settings()
    if settings.llm_provider != "openai":
        raise ValueError(f"不支援的 LLM 供應商：{settings.llm_provider}")
    return OpenAILLMClient(settings)
