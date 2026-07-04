"""檢查 LLM 產生的 SQL，只放行單一條唯讀 SELECT 敘述。"""

import re

from app.core.schema_context import ALLOWED_TABLES

_COMMENT_RE = re.compile(r"--|/\*")
_LIMIT_RE = re.compile(r"\blimit\b", re.IGNORECASE)
_TABLE_REF_RE = re.compile(
    r"\b(?:from|join)\s+([a-z_][a-z0-9_]*\.[a-z_][a-z0-9_]*)", re.IGNORECASE
)
# EXTRACT(MONTH FROM col) 的 FROM 不是子句，要先拿掉再抓表名，否則會誤判
_DATE_PART_KEYWORDS = (
    "century", "day", "decade", "dow", "doy", "epoch", "hour", "isodow",
    "isoyear", "microseconds", "millennium", "milliseconds", "minute",
    "month", "quarter", "second", "timezone", "timezone_hour",
    "timezone_minute", "week", "year",
)
_EXTRACT_FROM_RE = re.compile(
    r"\b(?:" + "|".join(_DATE_PART_KEYWORDS) + r")\s+from\s+"
    r"[a-z_][a-z0-9_]*(?:\.[a-z_][a-z0-9_]*)?",
    re.IGNORECASE,
)
_FORBIDDEN_KEYWORDS = (
    "insert", "update", "delete", "drop", "alter", "truncate", "grant",
    "revoke", "create", "copy", "call", "execute", "merge", "vacuum",
    "attach", "reindex", "cluster", "listen", "notify", "set", "reset",
    "lock", "prepare", "deallocate", "into", "pg_sleep",
)
_FORBIDDEN_RE = re.compile(
    r"\b(" + "|".join(_FORBIDDEN_KEYWORDS) + r")\b", re.IGNORECASE
)


class UnsafeSQLError(ValueError):
    """LLM 產生的 SQL 未通過安全檢查。"""


def ensure_safe_select(sql: str, max_rows: int = 200) -> str:
    stripped = sql.strip().rstrip(";").strip()
    if not stripped:
        raise UnsafeSQLError("SQL 為空")

    if ";" in stripped:
        raise UnsafeSQLError("只允許單一敘述，不可包含多條 SQL")

    if _COMMENT_RE.search(stripped):
        raise UnsafeSQLError("SQL 不可包含註解")

    if not re.match(r"^(select|with)\b", stripped, re.IGNORECASE):
        raise UnsafeSQLError("只允許 SELECT 查詢")

    if _FORBIDDEN_RE.search(stripped):
        raise UnsafeSQLError("SQL 包含不允許的關鍵字")

    if not _LIMIT_RE.search(stripped):
        stripped = f"{stripped} LIMIT {max_rows}"

    return stripped


def find_unknown_tables(sql: str) -> list[str]:
    """找出 FROM/JOIN 裡不在白名單內的資料表（多半是 LLM 幻覺出來的表名）。"""
    sql_without_date_extract = _EXTRACT_FROM_RE.sub("", sql)
    referenced = {
        match.group(1).lower() for match in _TABLE_REF_RE.finditer(sql_without_date_extract)
    }
    return sorted(referenced - ALLOWED_TABLES)
