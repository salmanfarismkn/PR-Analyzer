from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.check.models import CheckRun
from app.commit.models import Commit
from app.webhook.schemas import CheckRunWebhookPayload
from app.webhook.exceptions import WebhookDependencyPending
from app.pull_request.models import PullRequest
from app.feature.service import PRFeatureService
from app.application.outcome_evaluation import evaluate_pull_request_outcome

class CheckRunWebhookService:

    def __init__(self) -> None:
        self._feature_service = PRFeatureService()

    def process(
        self,
        db: Session,
        payload: CheckRunWebhookPayload,
    ) -> CheckRun | None:

        if payload.action not in {
            "created",
            "rerequested",
            "completed",
        }:
            return None

        check_data = payload.check_run

        commit = db.scalar(
            select(Commit).where(
                Commit.sha == check_data.head_sha
            )
        )

        if commit is None:
            raise WebhookDependencyPending(
                f"Commit {check_data.head_sha} "
                "has not been synchronized yet."
            )

        check_run = db.scalar(
            select(CheckRun).where(
                CheckRun.github_id == check_data.id
            )
        )

        if check_run is None:
            check_run = CheckRun(
                github_id=check_data.id,
                pull_request_id=commit.pull_request_id,
                name=check_data.name,
                status=check_data.status,
                conclusion=check_data.conclusion,
                details_url=check_data.details_url,
                started_at=check_data.started_at,
                completed_at=check_data.completed_at,
            )
            db.add(check_run)
        else:
            check_run.pull_request_id = commit.pull_request_id
            check_run.name = check_data.name
            check_run.status = check_data.status
            check_run.conclusion = check_data.conclusion
            check_run.details_url = check_data.details_url
            check_run.started_at = check_data.started_at
            check_run.completed_at = check_data.completed_at

        db.commit()
        db.refresh(check_run)

    
        pull_request = db.get(PullRequest, check_run.pull_request_id)

        if pull_request is not None:
            self._feature_service.create_snapshot(
                db=db,
                pull_request=pull_request,
            )
            
        evaluate_pull_request_outcome(
            db=db,
            pull_request_id=pull_request.id,
        )
        return check_run
