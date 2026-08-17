from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.webhook.models import WebhookEvent


class WebhookRetryService:

    def get_pending_events(
        self,
        db: Session,
        limit: int = 50,
    ) -> list[WebhookEvent]:

        return list(
            db.scalars(
                select(WebhookEvent)
                .where(
                    WebhookEvent.status == "pending"
                )
                .order_by(
                    WebhookEvent.created_at
                )
                .limit(limit)
            )
        )