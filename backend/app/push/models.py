from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import JSON, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
if TYPE_CHECKING:
    from app.repository.models import Repository


class PushEvent(BaseModel):
    __tablename__ = "push_event"

    delivery_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    repository_id: Mapped[int] = mapped_column(
        ForeignKey(
            "repository.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    before_sha: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
    )

    after_sha: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
    )

    ref: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    commit_count: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )

    commit_shas: Mapped[list] = mapped_column(
        JSON,
        nullable=True,
        default=list,
    )

    head_commit_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    repository: Mapped["Repository"] = relationship()

