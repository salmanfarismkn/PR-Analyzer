from __future__ import annotations

from sqlalchemy import ForeignKey, Index, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.pull_request.models import PullRequest


class RiskAssessment(BaseModel):
    __tablename__ = "risk_assessment"

    __table_args__ = (
        Index(
            "ix_risk_assessment_pull_request_id",
            "pull_request_id",
        ),
        Index(
            "ix_risk_assessment_score",
            "score",
        ),
    )

    pull_request_id: Mapped[int] = mapped_column(
        ForeignKey(
            "pull_requests.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    recommendation: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    metrics: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    categories: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
    )

    factors: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
    )

    pull_request: Mapped["PullRequest"] = relationship(
        back_populates="risk_assessments",
    )