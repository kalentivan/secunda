"""Роуты fastapi"""
import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Any, cast

import uvicorn
from dotenv import load_dotenv

from src.db.pre_load import run_fixtures
from src.db.session import AsyncSessionLocal

load_dotenv()

from src.core.logger import fastapi_logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware as CORS_Middleware
from starlette.requests import Request

from src.routes.routes import router as routes
from src.routes.logs import router as router_logs

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler для FastAPI."""
    logger.info("Starting application")
    async with AsyncSessionLocal() as session:
        from src.db.models import Building
        from sqlalchemy import select
        result = await session.execute(select(Building))
        if not result.scalars().first():
            await run_fixtures(session, "./static/fixtures.json")
            logger.info("Fixtures loaded during startup")
    yield
    logger.info("Shutting down application")

app = FastAPI(title="Встречи API", version="1.0.0")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
]

app.add_middleware(
    cast(Any, CORS_Middleware),  # иначе ругается
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------- #
app.include_router(routes)
app.include_router(router_logs)


logger = logging.getLogger(__name__)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        # Логируем ошибку через логгер
        logger.critical(
            f"Error in {request.method} {request.url}\nERROR: {str(e)}",
            exc_info=True,
            extra={
                "request_method": request.method,
                "request_url": str(request.url),
                "error_type": type(e).__name__
            }
        )
        raise  # Пробрасываем исключение дальше


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': '%(levelprefix)s %(message)s',
            'use_colors': None,
        },
        'access': {
            '()': 'uvicorn.logging.AccessFormatter',
            'fmt': '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
        },
    },
    'handlers': {
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'access': {
            'formatter': 'access',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        'uvicorn': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
        'uvicorn.error': {
            'level': 'INFO',
            'propagate': False
        },
        'uvicorn.access': {
            'handlers': ['access'],
            'level': 'INFO',
            'propagate': False
        },
        'fastapi': {
            'level': 'INFO',
            'propagate': False
        },
    },
}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
