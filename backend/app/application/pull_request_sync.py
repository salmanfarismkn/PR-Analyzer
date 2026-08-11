from sqlalchemy import select

from datetime import datetime

from sqlalchemy.orm import Session

from app.github.service import GitHubService
from app.pull_request.schemas import PullRequestImportSummary
from app.pull_request.service import PullRequestService
from app.repository.models import Repository
from app.pull_request.models import PullRequest


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

    @staticmethod
    def _normalize_datetime(value: object) -> datetime | None:
        if value in (None, ""):
            return None

        if isinstance(value, datetime):
            return value

        text = str(value).strip()
        if not text:
            return None

        if text.endswith("Z"):
            text = text[:-1] + "+00:00"

        return datetime.fromisoformat(text)

    def refresh_from_github(
        self,
        db: Session,
        repository: Repository,
        pull_request_data: dict,
    ) -> PullRequest:

        github_id = pull_request_data["id"]

        pull_request = db.scalar(
            select(PullRequest).where(
                PullRequest.github_id == github_id
            )
        )

        if pull_request is None:
            pull_request = PullRequest(
                repository_id=repository.id,
                github_id=pull_request_data["id"],
                number=pull_request_data["number"],
                title=pull_request_data["title"],
                author=pull_request_data.get("author", "unknown"),
                base_branch=pull_request_data.get("base_branch", "main"),
                head_branch=pull_request_data.get("head_branch", "unknown"),
                state=pull_request_data["state"],
                merged=pull_request_data["merged"],
                merged_at=self._normalize_datetime(pull_request_data.get("merged_at")),
                closed_at=self._normalize_datetime(pull_request_data.get("closed_at")),
            )

            db.add(pull_request)

        else:
            pull_request.title = pull_request_data["title"]
            pull_request.state = pull_request_data["state"]
            pull_request.merged = pull_request_data["merged"]
            pull_request.merged_at = self._normalize_datetime(
                pull_request_data.get("merged_at")
            )
            pull_request.closed_at = self._normalize_datetime(
                pull_request_data.get("closed_at")
            )

        db.commit()
        db.refresh(pull_request)

        return pull_request

    def sync_pull_request_data(
        self,
        db: Session,
        pull_request: PullRequest,
    ) -> None:
        return