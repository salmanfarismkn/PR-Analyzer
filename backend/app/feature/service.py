from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.commit.models import Commit
from app.pull_request.models import PullRequest
from app.review.models import Review
from app.check.models import CheckRun

from app.feature.schemas import PRFeatureSnapshot
from app.feature.models import PRFeatureSnapshot as PRFeatureSnapshotModel


class PRFeatureService:

    def build_snapshot(
        self,
        db: Session,
        pull_request: PullRequest,
    ) -> PRFeatureSnapshot:

        commits = list(
            db.scalars(
                select(Commit).where(
                    Commit.pull_request_id == pull_request.id
                )
            )
        )

        reviews = list(
            db.scalars(
                select(Review).where(
                    Review.pull_request_id == pull_request.id
                )
            )
        )

        checks = list(
            db.scalars(
                select(CheckRun).where(
                    CheckRun.pull_request_id == pull_request.id
                )
            )
        )

        additions = sum(
            getattr(commit, "additions", 0) or 0
            for commit in commits
        )

        deletions = sum(
            getattr(commit, "deletions", 0) or 0
            for commit in commits
        )

        unique_authors = {
            getattr(commit, "author_name", None)
            for commit in commits
            if getattr(commit, "author_name", None)
        }

        unique_reviewers = {
            getattr(review, "reviewer_login", None)
            for review in reviews
            if getattr(review, "reviewer_login", None)
        }

        approvals = sum(
            1 for review in reviews
            if review.state.upper() == "APPROVED"
        )

        change_requests = sum(
            1 for review in reviews
            if review.state.upper() == "CHANGES_REQUESTED"
        )

        successful_checks = sum(
            1 for check in checks
            if check.conclusion == "success"
        )

        failed_checks = sum(
            1 for check in checks
            if check.conclusion in {
                "failure", "cancelled", "timed_out", "action_required"
            }
        )

        pending_checks = sum(
            1 for check in checks
            if check.status not in {"completed"}
        )

        created_at = pull_request.created_at
        now = datetime.now(timezone.utc)

        age_hours = (
            max(
                0,
                (now - created_at).total_seconds() / 3600,
            )
            if created_at else 0
        )

        changed_files_list = getattr(pull_request, "changed_files", []) or []
        changed_files_count = len(changed_files_list)

        return PRFeatureSnapshot(
            pull_request_id=pull_request.id,

            additions=additions,
            deletions=deletions,
            changed_files=changed_files_count,  
            commit_count=len(commits),
            unique_authors=len(unique_authors),

            review_count=len(reviews),
            unique_reviewers=len(unique_reviewers),
            approvals=approvals,
            change_requests=change_requests,

            check_count=len(checks),
            successful_checks=successful_checks,
            failed_checks=failed_checks,
            pending_checks=pending_checks,

            is_draft=getattr(pull_request, "draft", False),


            age_hours=age_hours,
        )

    def save_snapshot(
        self,
        db: Session,
        snapshot: PRFeatureSnapshot,
    ) -> PRFeatureSnapshotModel:

        
        existing = db.scalar(
            select(PRFeatureSnapshotModel)
            .where(
                PRFeatureSnapshotModel.pull_request_id == snapshot.pull_request_id
            )
            .order_by(PRFeatureSnapshotModel.id.desc())
        )

        if existing is not None:
            same_state = (
                existing.additions == snapshot.additions
                and existing.deletions == snapshot.deletions
                and existing.changed_files == snapshot.changed_files
                and existing.commit_count == snapshot.commit_count
                and existing.review_count == snapshot.review_count
                and existing.approvals == snapshot.approvals
                and existing.change_requests == snapshot.change_requests
                and existing.check_count == snapshot.check_count
                and existing.successful_checks == snapshot.successful_checks
                and existing.failed_checks == snapshot.failed_checks
                and existing.pending_checks == snapshot.pending_checks
            )

            
            if same_state:
                return existing

        
        record = PRFeatureSnapshotModel(
            pull_request_id=snapshot.pull_request_id,

            additions=snapshot.additions,
            deletions=snapshot.deletions,
            changed_files=snapshot.changed_files,

            commit_count=snapshot.commit_count,
            unique_authors=snapshot.unique_authors,

            review_count=snapshot.review_count,
            unique_reviewers=snapshot.unique_reviewers,

            approvals=snapshot.approvals,
            change_requests=snapshot.change_requests,

            check_count=snapshot.check_count,
            successful_checks=snapshot.successful_checks,
            failed_checks=snapshot.failed_checks,
            pending_checks=snapshot.pending_checks,

            is_draft=snapshot.is_draft,

            age_hours=snapshot.age_hours,
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return record

    def create_snapshot(
        self,
        db: Session,
        pull_request: PullRequest,
    ) -> PRFeatureSnapshotModel:
        """
        Build a snapshot for the given pull request and save it.
        """
        snapshot = self.build_snapshot(
            db=db,
            pull_request=pull_request,
        )
        return self.save_snapshot(
            db=db,
            snapshot=snapshot,
        )