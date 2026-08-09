from __future__ import annotations

from sqlalchemy.orm import Session

from app.github.service import GitHubService
from app.pull_request.models import PullRequest
from app.review.schemas import ReviewImportSummary
from app.review.service import ReviewService


class ReviewSyncService:
    def __init__(self) -> None:
        self._github = GitHubService()
        self._review_service = ReviewService()

    def import_reviews(
        self,
        db: Session,
        pull_request: PullRequest,
    ) -> ReviewImportSummary:

        reviews = self._github.list_reviews(
            owner=pull_request.repository.owner,
            repository=pull_request.repository.name,
            pull_number=pull_request.number,
        )

        return self._review_service.import_reviews(
            db=db,
            pull_request_id=pull_request.id,
            reviews=reviews,
        )