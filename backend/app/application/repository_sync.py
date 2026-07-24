from sqlalchemy.orm import Session

from app.github.service import GitHubService
from app.repository.schemas import RepositoryImportSummary
from app.repository.service import RepositoryService


class RepositorySyncService:
    def __init__(self) -> None:
        self._github = GitHubService()
        self._repository_service = RepositoryService()

    def import_repositories(
        self,
        db: Session,
    ) -> RepositoryImportSummary:

        repositories = self._github.list_repositories()

        return self._repository_service.import_repositories(
            db=db,
            repositories=repositories,
        )