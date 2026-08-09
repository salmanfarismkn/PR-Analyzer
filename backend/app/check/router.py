from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.application.check_sync import CheckSyncService
from app.check.schemas import CheckRunImportSummary
from app.db.session import get_db
from app.pull_request.models import PullRequest


router = APIRouter(
    prefix="/check-runs",
    tags=["Check Runs"],
)

check_sync_service = CheckSyncService()


@router.post(
    "/import/{pull_request_id}",
    response_model=CheckRunImportSummary,
    status_code=HTTPStatus.OK,
)
def import_check_runs(
    pull_request_id: int,
    db: Session = Depends(get_db),
) -> CheckRunImportSummary:

    pull_request = db.get(
        PullRequest,
        pull_request_id,
    )

    if pull_request is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Pull request not found.",
        )

    return check_sync_service.import_check_runs(
        db=db,
        pull_request=pull_request,
    )