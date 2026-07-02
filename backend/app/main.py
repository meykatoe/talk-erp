"""FastAPI 應用程式進入點。"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import get_settings
from app.core.logging_config import setup_logging
from app.core.middleware import RequestLoggingMiddleware

settings = get_settings()
setup_logging(settings)

logger = logging.getLogger(__name__)

app = FastAPI(title=settings.project_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)

app.include_router(api_router, prefix=settings.api_v1_prefix)

logger.info("應用程式啟動完成，log 等級=%s", settings.log_level)
