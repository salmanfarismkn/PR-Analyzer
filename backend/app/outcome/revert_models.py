from __future__ import annotations

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.pull_request.models import PullRequest


class RevertEvent(BaseModel):
    __tablename__ = "revert_event"

    pull_request_id: Mapped[int] = mapped_column(
        ForeignKey(
            "pull_requests.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    revert_commit_sha: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
    )

    original_commit_sha: Mapped[str | None] = mapped_column(
        String(40),
        nullable=True,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    confidence: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="possible",
    )

    pull_request: Mapped["PullRequest"] = relationship()