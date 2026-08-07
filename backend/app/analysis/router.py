from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.analysis.service import AnalysisService
from app.analysis.schemas import PullRequestMetrics

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.get("/{pull_request_id}", response_model=PullRequestMetrics)
def get_pull_request_metrics(
    pull_request_id: int,
    db: Session = Depends(get_db),
) -> PullRequestMetrics:
    """
    Calculate and return metrics for a given pull request.
    """
    service = AnalysisService()
    return service.calculate_metrics(db=db, pull_request_id=pull_request_id)
