from sqlalchemy import select
from sqlalchemy.orm import Session
from app.repository.models import Repository
from app.repository.schemas import RepositoryImportSummary
from app.github.client import GitHubClient
from app.core.config import get_settings
from app.repository.service import import_repositories

class GitHubService:
    def __init__(self):
        settings = get_settings()
        self._client = GitHubClient(
            base_url=settings.github_api_url,
            token=settings.github_token,
        )

    def get_authenticated_user(self):
        return self._client.get_user()

    def import_user_repositories(self, db: Session) -> RepositoryImportSummary:
        # Fetch repositories from GitHub API
        repos = self._client.list_repositories()
        # Import them into DB
        summary = import_repositories(db, repos)
        return summary

    def list_repositories(self, db: Session) -> list[Repository]:
        # Query repositories stored in your DB
        return list(
            db.scalars(
                select(Repository).order_by(Repository.id)
            )
        )
