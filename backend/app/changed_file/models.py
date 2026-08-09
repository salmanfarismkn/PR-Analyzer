from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    Index,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.commit.models import Commit
    from app.pull_request.models import PullRequest


class ChangedFile(BaseModel):
    __tablename__ = "changed_files"

    __table_args__ = (
        Index("ix_changed_file_commit_id", "commit_id"),
        Index("ix_changed_file_filename", "filename"),
        Index("ix_changed_file_status", "status"),
        Index("ix_changed_file_pull_request_id", "pull_request_id"),  # ✅ index for PR lookups
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    commit_id: Mapped[int] = mapped_column(
        ForeignKey("commits.id", ondelete="CASCADE"),
        nullable=False,
    )

    pull_request_id: Mapped[int] = mapped_column(
        ForeignKey("pull_requests.id", ondelete="CASCADE"),
        nullable=False,
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    previous_filename: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    additions: Mapped[int] = mapped_column(nullable=False, default=0)
    deletions: Mapped[int] = mapped_column(nullable=False, default=0)
    changes: Mapped[int] = mapped_column(nullable=False, default=0)

    patch: Mapped[str | None] = mapped_column(Text, nullable=True)

    commit: Mapped["Commit"] = relationship(
        back_populates="changed_files",
    )

    pull_request: Mapped["PullRequest"] = relationship(
        back_populates="changed_files",
    )

