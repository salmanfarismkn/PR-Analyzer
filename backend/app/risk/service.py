from app.analysis.service import AnalysisService
from app.risk.engine import RiskEngine
from app.risk.schemas import PullRequestRisk


class RiskService:
    def __init__(self) -> None:
        self._analysis_service = AnalysisService()
        self._risk_engine = RiskEngine()

    def analyze_pull_request(
        self,
        db,
        pull_request_id: int,
    ) -> PullRequestRisk:

        metrics = self._analysis_service.calculate_metrics(
            db=db,
            pull_request_id=pull_request_id,
        )

        return self._risk_engine.calculate(
            pull_request_id=pull_request_id,
            metrics=metrics,
        )