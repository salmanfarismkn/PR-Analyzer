from __future__ import annotations

from sqlalchemy.orm import Session

from app.check.schemas import CheckRunImportSummary
from app.check.service import CheckRunService
from app.github.service import GitHubService
from app.pull_request.models import PullRequest


class CheckSyncService:

    def __init__(self) -> None:
        self._github = GitHubService()
        self._check_service = CheckRunService()

    def import_check_runs(
        self,
        db: Session,
        pull_request: PullRequest,
    ) -> CheckRunImportSummary:

        commits = self._github.list_commits(
            owner=pull_request.repository.owner,
            repository=pull_request.repository.name,
            pull_number=pull_request.number,
        )

        if not commits:
            return CheckRunImportSummary(
                imported=0,
                skipped=0,
                total=0,
            )

        latest_commit = commits[-1]

        check_runs = self._github.list_check_runs(
            owner=pull_request.repository.owner,
            repository=pull_request.repository.name,
            ref=latest_commit.sha,
        )

        return self._check_service.import_check_runs(
            db=db,
            pull_request_id=pull_request.id,
            check_runs=check_runs,
        )