from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.feature.schemas import PRFeatureSnapshot
from app.feature.service import PRFeatureService
from app.pull_request.models import PullRequest


router = APIRouter(
    prefix="/features",
    tags=["Features"],
)


service = PRFeatureService()


@router.get(
    "/pull-request/{pull_request_id}",
    response_model=PRFeatureSnapshot,
)
def get_pull_request_features(
    pull_request_id: int,
    db: Session = Depends(get_db),
) -> PRFeatureSnapshot:

    pull_request = db.get(
        PullRequest,
        pull_request_id,
    )

    if pull_request is None:
        raise HTTPException(
            status_code=404,
            detail="Pull request not found.",
        )

    return service.build_snapshot(
        db=db,
        pull_request=pull_request,
    )

@router.post(
    "/pull-request/{pull_request_id}/snapshot",
)
def create_pull_request_snapshot(
    pull_request_id: int,
    db: Session = Depends(get_db),
):

    pull_request = db.get(
        PullRequest,
        pull_request_id,
    )

    if pull_request is None:
        raise HTTPException(
            status_code=404,
            detail="Pull request not found.",
        )

    snapshot = service.build_snapshot(
        db=db,
        pull_request=pull_request,
    )

    record = service.save_snapshot(
        db=db,
        snapshot=snapshot,
    )

    return {
        "id": record.id,
        "pull_request_id": record.pull_request_id,
        "status": "created",
    }