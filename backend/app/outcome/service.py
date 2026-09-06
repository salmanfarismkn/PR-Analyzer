from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.check.models import CheckRun
from app.outcome.models import PullRequestOutcome
from app.pull_request.models import PullRequest
from app.review.models import Review
from app.outcome.revert_models import RevertEvent

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

        merged = getattr(pull_request, "merged", False)

        merged_at = getattr(
            pull_request,
            "merged_at",
            None,
        )

        state = getattr(
            pull_request,
            "state",
            None,
        )

        # -----------------------------------------
        # Lifecycle
        # -----------------------------------------

        if merged:
            outcome.lifecycle_status = "merged"
            outcome.merged_at = merged_at

        elif state == "closed":
            outcome.lifecycle_status = "closed"

        else:
            outcome.lifecycle_status = "pending"

        # -----------------------------------------
        # CI evidence
        # -----------------------------------------

        checks = (
            db.query(CheckRun)
            .filter(
                CheckRun.pull_request_id == pull_request.id
            )
            .all()
        )

        failed_checks = 0

        for check in checks:
            conclusion = getattr(
                check,
                "conclusion",
                None,
            )

            if conclusion in {
                "failure",
                "cancelled",
                "timed_out",
                "action_required",
            }:
                failed_checks += 1

        # -----------------------------------------
        # Review evidence
        # -----------------------------------------

        reviews = (
            db.query(Review)
            .filter(
                Review.pull_request_id == pull_request.id
            )
            .all()
        )

        change_requests = sum(
            1
            for review in reviews
            if getattr(review, "state", None)
            == "CHANGES_REQUESTED"
        )
        # -----------------------------------------
        # Revert evidence
        # -----------------------------------------

        revert_event = (
            db.query(RevertEvent)
            .filter(
                RevertEvent.pull_request_id == pull_request.id
            )
            .first()
        )

        was_reverted = revert_event is not None
        # -----------------------------------------
        # Quality classification
        # -----------------------------------------

        if not merged:
            outcome.outcome = "uncertain"
            outcome.reason = "PR has not been merged"

        elif was_reverted:
            outcome.outcome = "problematic"
            outcome.reason = "PR was later reverted"

        elif failed_checks > 0:
            outcome.outcome = "problematic"
            outcome.reason = "Merged PR had CI failures"

        elif change_requests > 0:
            outcome.outcome = "problematic"
            outcome.reason = "Merged PR had requested changes"

        else:
            outcome.outcome = "healthy"
            outcome.reason = "Merged without detected problems"

        outcome.observed_at = datetime.now(timezone.utc)

        db.add(outcome)
        db.commit()
        db.refresh(outcome)

        return outcome