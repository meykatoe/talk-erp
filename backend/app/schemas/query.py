"""Text-to-SQL 查詢的請求／回應格式。"""

from pydantic import BaseModel, Field


class StructuredQueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)


class StructuredQueryResponse(BaseModel):
    question: str
    sql: str
    columns: list[str]
    rows: list[dict]
    answer: str
