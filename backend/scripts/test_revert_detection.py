from sqlalchemy import select

from app.application.revert_detection import (
    RevertDetectionService,
)
from app.commit.models import Commit
from app.db.session import SessionLocal
from app.repository.models import Repository


db = SessionLocal()

try:
    revert_commit = db.scalar(
        select(Commit)
        .order_by(Commit.id.desc())
    )

    if revert_commit is None:
        raise RuntimeError(
            "No commits found."
        )

    repository = db.get(
        Repository,
        1,
    )

    if repository is None:
        raise RuntimeError(
            "Repository not found."
        )

    service = RevertDetectionService()

    result = service.inspect_commit(
        db=db,
        repository_owner=repository.owner,
        repository_name=repository.name,
        commit_sha=revert_commit.sha,
    )

    print("Result:", result)

finally:
    db.close()