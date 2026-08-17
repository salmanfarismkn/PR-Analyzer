from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.push.models import PushEvent
from app.repository.models import Repository
from app.webhook.schemas import PushWebhookPayload


class PushWebhookService:

    def process(
        self,
        db: Session,
        delivery_id: str,
        payload: PushWebhookPayload,
    ) -> PushEvent | None:

        repository = db.scalar(
            select(Repository).where(
                Repository.owner == payload.repository.owner["login"],
                Repository.name == payload.repository.name
            )
        )

        if repository is None:
            raise ValueError(
                f"Repository {payload.repository.owner.login}/{payload.repository.name} "
                "from push webhook does not exist locally."
            )

        existing = db.scalar(
            select(PushEvent).where(
                PushEvent.delivery_id == delivery_id
            )
        )
        if existing is not None:
            return existing

        head_commit_message = None
        if payload.head_commit is not None:
            head_commit_message = payload.head_commit.message

        push_event = PushEvent(
            delivery_id=delivery_id,
            repository_id=repository.id,
            before_sha=payload.before,
            after_sha=payload.after,
            ref=payload.ref,
            commit_count=len(payload.commits),
            head_commit_message=head_commit_message,
        )

        db.add(push_event)
        db.commit()
        db.refresh(push_event)

        return push_event
