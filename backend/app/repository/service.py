from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import RepositoryAlreadyExistsError
from app.repository.models import Repository
from app.repository.schemas import RepositoryCreate


def create_repository(
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

    repository = Repository(**data.model_dump())

    db.add(repository)
    db.commit()
    db.refresh(repository)

    return repository


def list_repositories(
    db: Session,
) -> list[Repository]:
    return list(
        db.scalars(
            select(Repository).order_by(Repository.id)
        )
    )