from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.github.schemas import GitHubPullRequest
from app.pull_request.models import PullRequest
from app.pull_request.schemas import PullRequestImportSummary


class PullRequestService:
    def import_pull_requests(
        self,
        db: Session,
        repository_id: int,
        pull_requests: list[GitHubPullRequest],
    ) -> PullRequestImportSummary:
        imported = 0
        skipped = 0

        existing_ids = set(
            db.scalars(
                select(PullRequest.github_id).where(
                    PullRequest.repository_id == repository_id
                )
            ).all()
        )

        for pr in pull_requests:
            if pr.id in existing_ids:
                skipped += 1
                continue

            db.add(
                PullRequest(
                    github_id=pr.id,
                    repository_id=repository_id,
                    number=pr.number,
                    title=pr.title,
                    state=pr.state,
                    author=pr.user.login,
                    base_branch=pr.base.ref,
                    head_branch=pr.head.ref,
                    is_draft=pr.draft,
                )
            )
            imported += 1

        db.commit()

        return PullRequestImportSummary(
            imported=imported,
            skipped=skipped,
            total=len(pull_requests),
        )

    def list_pull_requests(self, db: Session, repository_id: int) -> list[PullRequest]:
        return list(
            db.scalars(
                select(PullRequest).where(
                    PullRequest.repository_id == repository_id
                ).order_by(PullRequest.number)
            )
        )

    def get_pull_request_by_id(self, db: Session, pr_id: int) -> PullRequest | None:
        return db.scalar(
            select(PullRequest).where(PullRequest.id == pr_id)
        )
