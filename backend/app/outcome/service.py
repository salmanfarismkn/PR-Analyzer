from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.outcome.models import PullRequestOutcome
from app.pull_request.models import PullRequest


class PullRequestOutcomeService:

    def record_merge(
        self,
        db: Session,
        pull_request: PullRequest,
    ) -> PullRequestOutcome:

        outcome = pull_request.outcome

        if outcome is None:
            outcome = PullRequestOutcome(
                pull_request_id=pull_request.id,
                status="merged",
                merged_at=pull_request.merged_at,
                observed_at=datetime.now(timezone.utc),
            )

            db.add(outcome)

        else:
            outcome.status = "merged"
            outcome.merged_at = (
                pull_request.merged_at
            )
            outcome.observed_at = (
                datetime.now(timezone.utc)
            )

        db.commit()
        db.refresh(outcome)

        return outcome