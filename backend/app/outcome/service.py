from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.check.models import CheckRun
from app.outcome.models import PullRequestOutcome
from app.pull_request.models import PullRequest
from app.review.models import Review


class OutcomeEvaluator:

    def evaluate(
        self,
        db: Session,
        pull_request: PullRequest,
    ) -> PullRequestOutcome:

        outcome = (
            db.query(PullRequestOutcome)
            .filter(
                PullRequestOutcome.pull_request_id == pull_request.id
            )
            .first()
        )

        if outcome is None:
            outcome = PullRequestOutcome(
                pull_request_id=pull_request.id,
            )
            db.add(outcome)

        # -------------------------------------------------
        # 1. Determine merge state
        # -------------------------------------------------

        merged = getattr(pull_request, "merged", False)

        merged_at = getattr(pull_request, "merged_at", None)

        if merged:
            outcome.status = "merged"
            outcome.merged_at = merged_at

        else:
            outcome.status = "pending"

        # -------------------------------------------------
        # 2. Check CI results
        # -------------------------------------------------

        checks = (
            db.query(CheckRun)
            .filter(
                CheckRun.pull_request_id == pull_request.id
            )
            .all()
        )

        failed_checks = 0

        for check in checks:
            conclusion = getattr(check, "conclusion", None)

            if conclusion in {
                "failure",
                "cancelled",
                "timed_out",
                "action_required",
            }:
                failed_checks += 1

        # -------------------------------------------------
        # 3. Review signals
        # -------------------------------------------------

        reviews = (
            db.query(Review)
            .filter(
                Review.pull_request_id == pull_request.id
            )
            .all()
        )

        change_requests = 0

        for review in reviews:
            state = getattr(review, "state", None)

            if state == "CHANGES_REQUESTED":
                change_requests += 1

        # -------------------------------------------------
        # 4. Determine outcome
        # -------------------------------------------------

        if merged:

            if failed_checks > 0 or change_requests > 0:
                outcome.reason = (
                    "Merged PR with CI failures or requested changes"
                )
            else:
                outcome.reason = "Merged successfully"

        else:
            outcome.reason = "PR has not been merged yet"

        outcome.observed_at = datetime.now(timezone.utc)

        db.add(outcome)
        db.commit()
        db.refresh(outcome)

        return outcome