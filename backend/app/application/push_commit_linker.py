from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.commit.models import Commit
from app.push.models import PushEvent


class PushCommitLinker:

    def find_existing_commits(
        self,
        db: Session,
        push_event: PushEvent,
    ) -> list[Commit]:

        if not push_event.commit_shas:
            return []

        return list(
            db.scalars(
                select(Commit).where(
                    Commit.sha.in_(
                        push_event.commit_shas
                    )
                )
            )
        )