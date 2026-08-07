from fastapi import APIRouter

from app.health.router import router as health_router
from app.repository.router import router as repository_router
from app.github.router import router as github_router
from app.pull_request.router import router as pull_request_router
from app.commit.router import router as commit_router
from app.analysis.router import router as analysis_router
from app.changed_file.router import router as changed_file_router

router = APIRouter()

router.include_router(health_router)
router.include_router(repository_router)
router.include_router(github_router)
router.include_router(pull_request_router)
router.include_router(commit_router)
router.include_router(analysis_router)
router.include_router(changed_file_router)