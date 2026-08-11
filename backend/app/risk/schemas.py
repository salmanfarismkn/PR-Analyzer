from datetime import datetime

from pydantic import BaseModel, Field

from app.analysis.schemas import PullRequestMetrics


class RiskFactor(BaseModel):
    name: str
    category: str
    score: int
    severity: str
    reason: str
    recommendation: str


class RiskCategory(BaseModel):
    name: str
    score: int
    factors: list[str]


class PullRequestRisk(BaseModel):
    pull_request_id: int

    score: int = Field(
        ge=0,
        le=100,
    )

    level: str

    recommendation: str

    categories: list[RiskCategory]

    factors: list[RiskFactor]

    metrics: PullRequestMetrics


class RiskAssessmentResponse(PullRequestRisk):
    assessment_id: int
    created_at: datetime


class RiskAssessmentSummary(BaseModel):
    assessment_id: int
    pull_request_id: int
    score: int
    level: str
    created_at: datetime