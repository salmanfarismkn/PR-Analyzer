from sqlalchemy import (
    BigInteger,
    Boolean,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel
from sqlalchemy.orm import relationship

from app.repository.models import Repository
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.repository.models import Repository

class PullRequest(BaseModel):
    __tablename__ = "pull_request"

    __table_args__ = (
        UniqueConstraint(
            "repository_id",
            "github_id",
            name="uq_pull_request_repository_github",
        ),
        Index("ix_pull_request_repository_id", "repository_id"),
        Index("ix_pull_request_github_id", "github_id"),
        Index("ix_pull_request_state", "state"),
    )

    github_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    repository_id: Mapped[int] = mapped_column(
        ForeignKey(
            "repository.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    number: Mapped[int] = mapped_column(
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
    )

    state: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    author: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    base_branch: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    head_branch: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    is_draft: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    repository: Mapped["Repository"] = relationship(
        back_populates="pull_requests",
    )