from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.application.pull_request_sync import PullRequestSyncService
from app.db.session import get_db
from app.pull_request.schemas import PullRequestImportSummary
from app.repository.models import Repository

router = APIRouter(
    prefix="/pull-requests",
    tags=["Pull Requests"],
)

pull_request_sync_service = PullRequestSyncService()


@router.post(
    "/import/{repository_id}",
    response_model=PullRequestImportSummary,
    status_code=HTTPStatus.OK,
)
def import_pull_requests(
    repository_id: int,
    db: Session = Depends(get_db),
) -> PullRequestImportSummary:

    repository = db.get(Repository, repository_id)

    if repository is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Repository not found.",
        )

    return pull_request_sync_service.import_pull_requests(
        db=db,
        repository=repository,
    )