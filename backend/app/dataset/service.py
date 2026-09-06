from sqlalchemy.orm import Session

from app.feature.models import PRFeatureSnapshot
from app.outcome.models import PullRequestOutcome
from datetime import timezone

class TrainingDatasetService:

    def build_dataset(
        self,
        db: Session,
    ) -> list[dict]:

        outcomes = (
            db.query(PullRequestOutcome)
            .filter(
                PullRequestOutcome.outcome.in_(
                    ["healthy", "problematic"]
                )
            )
            .all()
        )

        dataset = []

        for outcome in outcomes:

            # -----------------------------------------
            # Find snapshots belonging to this PR
            # -----------------------------------------

            snapshots = (
                db.query(PRFeatureSnapshot)
                .filter(
                    PRFeatureSnapshot.pull_request_id
                    == outcome.pull_request_id
                )
                .order_by(
                    PRFeatureSnapshot.created_at.asc()
                )
                .all()
            )

            if not snapshots:
                continue

            # -----------------------------------------
            # Find the latest snapshot before outcome
            # -----------------------------------------

            valid_snapshots = [
                snapshot
                for snapshot in snapshots
                if snapshot.created_at.astimezone(timezone.utc)
                <= outcome.observed_at.astimezone(timezone.utc)
            ]


            if not valid_snapshots:
                continue

            snapshot = valid_snapshots[-1]

            # -----------------------------------------
            # Build training example
            # -----------------------------------------

            dataset.append(
                {
                    "pull_request_id": snapshot.pull_request_id,

                    "additions": snapshot.additions,
                    "deletions": snapshot.deletions,
                    "changed_files": snapshot.changed_files,
                    "commit_count": snapshot.commit_count,

                    "unique_authors": snapshot.unique_authors,
                    "review_count": snapshot.review_count,
                    "unique_reviewers": snapshot.unique_reviewers,
                    "approvals": snapshot.approvals,
                    "change_requests": snapshot.change_requests,

                    "check_count": snapshot.check_count,
                    "successful_checks": snapshot.successful_checks,
                    "failed_checks": snapshot.failed_checks,
                    "pending_checks": snapshot.pending_checks,

                    "is_draft": snapshot.is_draft,
                    "age_hours": snapshot.age_hours,

                    "label": outcome.outcome,
                }
            )

        return dataset