from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.pull_request.models import PullRequest
from app.risk.schemas import PullRequestRisk
from app.risk.service import RiskService


router = APIRouter(
    prefix="/risk",
    tags=["Risk Analysis"],
)

risk_service = RiskService()


@router.get(
    "/pull-request/{pull_request_id}",
    response_model=PullRequestRisk,
    status_code=HTTPStatus.OK,
)
def analyze_pull_request(
    pull_request_id: int,
    db: Session = Depends(get_db),
) -> PullRequestRisk:

    pull_request = db.get(
        PullRequest,
        pull_request_id,
    )

    if pull_request is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Pull request not found.",
        )

    return risk_service.analyze_pull_request(
        db=db,
        pull_request_id=pull_request_id,
    )