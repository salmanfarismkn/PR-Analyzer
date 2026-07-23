from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.github.schemas import GitHubUser
from app.github.service import GitHubService
from app.db.session import get_db
from app.repository.schemas import RepositoryImportSummary

router = APIRouter(
    prefix="/github",
    tags=["GitHub"],
)

# Instantiate service with no arguments (self-configures via get_settings)
service = GitHubService()

@router.get("/me", response_model=GitHubUser)
def get_me():
    return service.get_authenticated_user()

@router.post("/repositories/import", response_model=RepositoryImportSummary)
def import_repositories_endpoint(db: Session = Depends(get_db)):
    return service.import_user_repositories(db)

@router.get("/repositories")
def list_repositories_endpoint(db: Session = Depends(get_db)):
    return service.list_repositories(db)
