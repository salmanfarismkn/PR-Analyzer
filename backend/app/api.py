from fastapi import APIRouter

from app.health.router import router as health_router
from app.repository.router import router as repository_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(repository_router)