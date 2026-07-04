"""Text-to-SQL 查詢的請求／回應格式。"""

from pydantic import BaseModel, Field

# 最多紀錄對話輪次3輪
MAX_HISTORY_TURNS = 3


class ConversationTurn(BaseModel):
    question: str
    answer: str


class StructuredQueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    # 只保留寬鬆上限防濫用，實際只取最近 MAX_HISTORY_TURNS 輪由端點處理
    history: list[ConversationTurn] = Field(default_factory=list, max_length=20)


class StructuredQueryResponse(BaseModel):
    question: str
    sql: str
    columns: list[str]
    rows: list[dict]
    answer: str
    is_relevant: bool = True
