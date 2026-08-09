from pydantic import BaseModel, Field

from app.analysis.schemas import PullRequestMetrics


class RiskFactor(BaseModel):
    name: str
    score: int
    reason: str


class PullRequestRisk(BaseModel):
    pull_request_id: int

    score: int = Field(
        ge=0,
        le=100,
    )

    level: str

    factors: list[RiskFactor]

    metrics: PullRequestMetrics