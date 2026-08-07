from sqlalchemy import select
from sqlalchemy.orm import Session
from app.repository.models import Repository
from app.repository.schemas import RepositoryImportSummary
from app.github.client import GitHubClient
from app.core.config import get_settings

from app.github.schemas import GitHubChangedFile, GitHubPullRequest
from app.pull_request.schemas import PullRequestImportSummary
from app.github.schemas import GitHubCommit


class GitHubService:
    def __init__(self):
        settings = get_settings()
        self._client = GitHubClient(
            base_url=settings.github_api_url,
            token=settings.github_token,
        )

    def get_authenticated_user(self):
        return self._client.get_user()


    def list_repositories(self, db: Session) -> list[Repository]:
        # Query repositories stored in your DB
        return list(
            db.scalars(
                select(Repository).order_by(Repository.id)
            )
        )

    def list_pull_requests(
        self,
        owner: str,
        repository: str,
    ) -> list[GitHubPullRequest]:
        return self._client.list_pull_requests(
            owner,
            repository,
        )

    def list_commits(
        self,
        owner: str,
        repository: str,
        pull_number: int,
    ) -> list[GitHubCommit]:
        return self._client.list_commits(
            owner,
            repository,
            pull_number,
        )
    
    def list_changed_files(
        self,
        owner: str,
        repository: str,
        pull_number: int,
    ) -> list[GitHubChangedFile]:
        return self._client.list_changed_files(owner, repository, pull_number)
