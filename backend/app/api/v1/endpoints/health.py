"""健康檢查端點，用於確認服務與資料庫連線狀態。"""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
def check_health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/db")
def check_database(db: Session = Depends(get_db)) -> dict[str, str]:
    db.execute(text("SELECT 1"))
    return {"status": "ok"}
