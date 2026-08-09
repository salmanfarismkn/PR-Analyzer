from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.check.models import CheckRun
from app.check.schemas import CheckRunImportSummary
from app.github.schemas import GitHubCheckRun


class CheckRunService:

    def import_check_runs(
        self,
        db: Session,
        pull_request_id: int,
        check_runs: list[GitHubCheckRun],
    ) -> CheckRunImportSummary:

        imported = 0
        skipped = 0

        existing_ids = set(
            db.scalars(
                select(CheckRun.github_id).where(
                    CheckRun.pull_request_id == pull_request_id
                )
            ).all()
        )

        for check in check_runs:

            if check.id in existing_ids:
                skipped += 1
                continue

            db.add(
                CheckRun(
                    github_id=check.id,
                    pull_request_id=pull_request_id,
                    name=check.name,
                    status=check.status,
                    conclusion=check.conclusion,
                    details_url=check.details_url,
                    started_at=check.started_at,
                    completed_at=check.completed_at,
                )
            )

            imported += 1

        db.commit()

        return CheckRunImportSummary(
            imported=imported,
            skipped=skipped,
            total=len(check_runs),
        )

    def list_check_runs(
        self,
        db: Session,
        pull_request_id: int,
    ) -> list[CheckRun]:

        return list(
            db.scalars(
                select(CheckRun)
                .where(
                    CheckRun.pull_request_id == pull_request_id
                )
                .order_by(CheckRun.id)
            )
        )