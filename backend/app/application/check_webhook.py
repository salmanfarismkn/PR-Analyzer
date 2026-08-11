from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.check.models import CheckRun
from app.commit.models import Commit
from app.webhook.schemas import CheckRunWebhookPayload


class CheckRunWebhookService:

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
            raise ValueError(
                "Commit from check-run webhook "
                "does not exist locally."
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
            check_run.pull_request_id = (
                commit.pull_request_id
            )

            check_run.name = check_data.name
            check_run.status = check_data.status
            check_run.conclusion = check_data.conclusion
            check_run.details_url = check_data.details_url
            check_run.started_at = check_data.started_at
            check_run.completed_at = check_data.completed_at

        db.commit()
        db.refresh(check_run)

        return check_run