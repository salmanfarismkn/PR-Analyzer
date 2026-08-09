from sqlalchemy.orm import Session

from app.github.service import GitHubService
from app.pull_request.schemas import PullRequestImportSummary
from app.pull_request.service import PullRequestService
from app.repository.models import Repository


class PullRequestSyncService:
    def __init__(self) -> None:
        self._github = GitHubService()
        self._pull_request_service = PullRequestService()

    def import_pull_requests(
        self,
        db: Session,
        repository: Repository,
    ) -> PullRequestImportSummary:

        pull_requests = self._github.list_pull_requests(
            owner=repository.owner,
            repository=repository.name,
        )

        self._pull_request_service.import_pull_requests(
            db=db,
            repository_id=repository.id,
            pull_requests=pull_requests,
        )