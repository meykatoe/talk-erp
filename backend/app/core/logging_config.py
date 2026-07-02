"""日誌設定，統一輸出至主控台與檔案（依日期輪替）。"""

import logging.config
from pathlib import Path

from app.core.config import Settings

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def setup_logging(settings: Settings) -> None:
    log_dir = Path(settings.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {"format": LOG_FORMAT},
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": settings.log_level,
                },
                "app_file": {
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "formatter": "default",
                    "filename": str(log_dir / "app.log"),
                    "when": "midnight",
                    "backupCount": 30,
                    "encoding": "utf-8",
                    "level": settings.log_level,
                },
                "error_file": {
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "formatter": "default",
                    "filename": str(log_dir / "error.log"),
                    "when": "midnight",
                    "backupCount": 30,
                    "encoding": "utf-8",
                    "level": "ERROR",
                },
            },
            "root": {
                "handlers": ["console", "app_file", "error_file"],
                "level": settings.log_level,
            },
            "loggers": {
                # 讓 uvicorn 的 log 也統一走 root 的 handlers，避免分散在兩處
                "uvicorn": {"handlers": [], "level": settings.log_level, "propagate": True},
                "uvicorn.error": {"handlers": [], "level": settings.log_level, "propagate": True},
                "uvicorn.access": {"handlers": [], "level": settings.log_level, "propagate": True},
                # SQL 語法太吵，預設只留 WARNING 以上
                "sqlalchemy.engine": {"handlers": [], "level": "WARNING", "propagate": True},
            },
        }
    )
