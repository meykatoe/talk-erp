"""SQLAlchemy 引擎與 session 管理。"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()

engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)

SessionLocal = sessionmaker(
    bind=engine, autocommit=False, autoflush=False, future=True
)

# 唯讀帳號的獨立引擎，statement_timeout / read-only 已在資料庫角色層設定
readonly_engine = create_engine(
    settings.readonly_database_url, pool_pre_ping=True, future=True
)

ReadonlySessionLocal = sessionmaker(
    bind=readonly_engine, autocommit=False, autoflush=False, future=True
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_readonly_db() -> Generator[Session, None, None]:
    db = ReadonlySessionLocal()
    try:
        yield db
    finally:
        db.close()
