from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.analysis.schemas import PullRequestMetrics
from app.analysis.service import AnalysisService
from app.db.session import get_db
from app.pull_request.models import PullRequest


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)

analysis_service = AnalysisService()


@router.get(
    "/{pull_request_id}",
    response_model=PullRequestMetrics,
    status_code=HTTPStatus.OK,
)
def get_pull_request_metrics(
    pull_request_id: int,
    db: Session = Depends(get_db),
) -> PullRequestMetrics:

    pull_request = db.get(
        PullRequest,
        pull_request_id,
    )

    if pull_request is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Pull request not found.",
        )

    return analysis_service.calculate_metrics(
        db=db,
        pull_request_id=pull_request_id,
    )
