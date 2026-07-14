from fastapi import FastAPI

from app.api.router import router
from app.core.config import settings
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/")
async def root():
    return {
        "application": settings.app_name,
        "status": "running",
        "version": "0.1.0",
    }

app.include_router(router)