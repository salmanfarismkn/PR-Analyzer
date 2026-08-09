from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import RepositoryAlreadyExistsError
from app.github.schemas import GitHubRepository
from app.repository.models import Repository
from app.repository.schemas import (
    RepositoryCreate,
    RepositoryImportSummary,
)


class RepositoryService:
    """Handles persistence and queries for Repository entities."""

    def create_repository(
        self,
        db: Session,
        data: RepositoryCreate,
    ) -> Repository:
        existing = db.scalar(
            select(Repository).where(
                Repository.github_id == data.github_id
            )
        )

        if existing:
            raise RepositoryAlreadyExistsError(
                f"Repository with GitHub ID {data.github_id} already exists."
            )

        repository = Repository(
            github_id=data.github_id,
            owner=data.owner,
            name=data.name,
            description=data.description,
            default_branch=data.default_branch,
            is_private=data.is_private,
        )

        db.add(repository)
        db.commit()
        db.refresh(repository)

        return repository

    def list_repositories(
        self,
        db: Session,
    ) -> list[Repository]:
        return list(
            db.scalars(
                select(Repository).order_by(Repository.id)
            )
        )

    def get_repository_by_id(
        self,
        db: Session,
        repository_id: int,
    ) -> Repository | None:
        return db.get(Repository, repository_id)

    def get_repository_by_github_id(
        self,
        db: Session,
        github_id: int,
    ) -> Repository | None:
        return db.scalar(
            select(Repository).where(
                Repository.github_id == github_id
            )
        )

    def import_repositories(
        self,
        db: Session,
        repositories: list[GitHubRepository],
    ) -> RepositoryImportSummary:

        imported = 0
        skipped = 0

        existing_ids = set(
            db.scalars(
                select(Repository.github_id)
            ).all()
        )

        for repo in repositories:

            if repo.id in existing_ids:
                skipped += 1
                continue

            repository = Repository(
                github_id=repo.id,
                owner=repo.owner.login,
                name=repo.name,
                description=repo.description,
                default_branch=repo.default_branch,
                is_private=repo.private,
            )

            db.add(repository)
            imported += 1

        db.commit()

        return RepositoryImportSummary(
            imported=imported,
            skipped=skipped,
            total=len(repositories),
        )