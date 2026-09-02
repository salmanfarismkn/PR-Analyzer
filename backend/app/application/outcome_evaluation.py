from sqlalchemy.orm import Session

from app.outcome.service import OutcomeEvaluator
from app.pull_request.models import PullRequest


def evaluate_pull_request_outcome(
    db: Session,
    pull_request_id: int,
):
    pull_request = (
        db.query(PullRequest)
        .filter(PullRequest.id == pull_request_id)
        .first()
    )

    if pull_request is None:
        return None

    evaluator = OutcomeEvaluator()

    return evaluator.evaluate(
        db=db,
        pull_request=pull_request,
    )