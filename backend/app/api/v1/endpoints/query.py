"""Text-to-SQL 查詢端點：自然語言問題轉 SQL，唯讀執行後生成回答。"""

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.database import get_readonly_db
from app.core.llm import LLMClient, get_llm_client
from app.core.schema_context import SCHEMA_CONTEXT
from app.core.sql_guard import UnsafeSQLError, ensure_safe_select, find_unknown_tables
from app.schemas.query import StructuredQueryRequest, StructuredQueryResponse

router = APIRouter(prefix="/query", tags=["query"])
logger = logging.getLogger("app.query")

MAX_SQL_ATTEMPTS = 2


def _generate_and_run_sql(
    llm: LLMClient, db: Session, question: str
) -> tuple[str, list[str], list[dict]]:
    previous_sql: str | None = None
    previous_error: str | None = None
    last_exc: Exception | None = None

    for attempt in range(1, MAX_SQL_ATTEMPTS + 1):
        try:
            sql = llm.generate_sql(question, SCHEMA_CONTEXT, previous_sql, previous_error)
        except Exception as exc:
            logger.exception("LLM 產生 SQL 失敗 question=%s", question)
            raise HTTPException(status_code=502, detail="LLM 產生 SQL 失敗") from exc

        try:
            safe_sql = ensure_safe_select(sql)
        except UnsafeSQLError as exc:
            logger.warning(
                "LLM 產生的 SQL 未通過安全檢查 question=%s sql=%s reason=%s",
                question,
                sql,
                exc,
            )
            raise HTTPException(status_code=422, detail=f"查詢無法執行：{exc}") from exc

        unknown_tables = find_unknown_tables(safe_sql)
        if unknown_tables:
            reason = f"使用了不存在或未授權的資料表：{', '.join(unknown_tables)}"
            logger.warning(
                "SQL 引用未知資料表（第 %d/%d 次）question=%s sql=%s tables=%s",
                attempt,
                MAX_SQL_ATTEMPTS,
                question,
                safe_sql,
                unknown_tables,
            )
            previous_sql, previous_error = safe_sql, reason
            last_exc = UnsafeSQLError(reason)
            continue

        try:
            result = db.execute(text(safe_sql))
            columns = list(result.keys())
            rows = [dict(row) for row in result.mappings().all()]
            return safe_sql, columns, rows
        except SQLAlchemyError as exc:
            logger.warning(
                "SQL 執行失敗（第 %d/%d 次）question=%s sql=%s error=%s",
                attempt,
                MAX_SQL_ATTEMPTS,
                question,
                safe_sql,
                exc,
            )
            db.rollback()
            previous_sql, previous_error = safe_sql, str(exc)
            last_exc = exc

    raise HTTPException(
        status_code=422, detail="查詢執行失敗，請換個問法再試"
    ) from last_exc


@router.post("/structured", response_model=StructuredQueryResponse)
def query_structured(
    payload: StructuredQueryRequest,
    db: Session = Depends(get_readonly_db),
    llm: LLMClient = Depends(get_llm_client),
) -> StructuredQueryResponse:
    safe_sql, columns, rows = _generate_and_run_sql(llm, db, payload.question)

    try:
        answer = llm.generate_answer(payload.question, safe_sql, rows)
    except Exception as exc:
        logger.exception("LLM 產生回答失敗 question=%s", payload.question)
        raise HTTPException(status_code=502, detail="LLM 產生回答失敗") from exc

    logger.info(
        "structured query 完成 question=%s row_count=%d", payload.question, len(rows)
    )
    return StructuredQueryResponse(
        question=payload.question,
        sql=safe_sql,
        columns=columns,
        rows=rows,
        answer=answer,
    )
