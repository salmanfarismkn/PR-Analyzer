from sqlalchemy import (
    BigInteger,
    Boolean,
    String,
    Text,
    UniqueConstraint,
    Index,
)

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel
from sqlalchemy.orm import relationship


class Repository(BaseModel):
    __tablename__ = "repository"

    __table_args__ = (
        UniqueConstraint("github_id", name="uq_repository_github_id"),
        UniqueConstraint("owner", "name", name="uq_repository_owner_name"),
        Index("ix_repository_owner", "owner"),
    )

    github_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    owner: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    default_branch: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="main",
    )

    is_private: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    pull_requests: Mapped[list["PullRequest"]] = relationship(
        back_populates="repository",
        cascade="all, delete-orphan",
    )