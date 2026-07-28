from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.pull_request.models import PullRequest


class Commit(BaseModel):
    __tablename__ = "commits"

    __table_args__ = (
        UniqueConstraint(
            "sha",
            name="uq_commit_sha",
        ),
        Index(
            "ix_commit_pull_request_id",
            "pull_request_id",
        ),
        Index(
            "ix_commit_sha",
            "sha",
        ),
    )

    pull_request_id: Mapped[int] = mapped_column(
        ForeignKey(
            "pull_requests.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    sha: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    author_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    author_email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    committed_at: Mapped[datetime]

    pull_request: Mapped["PullRequest"] = relationship(
        back_populates="commits",
    )