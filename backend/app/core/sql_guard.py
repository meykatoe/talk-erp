"""檢查 LLM 產生的 SQL，只放行單一條唯讀 SELECT 敘述。"""

import re

_COMMENT_RE = re.compile(r"--|/\*")
_LIMIT_RE = re.compile(r"\blimit\b", re.IGNORECASE)
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
