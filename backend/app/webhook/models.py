from sqlalchemy import Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class WebhookEvent(BaseModel):
    __tablename__ = "webhook_event"

    __table_args__ = (
        Index(
            "ix_webhook_event_event_type",
            "event_type",
        ),
        Index(
            "ix_webhook_event_status",
            "status",
        ),
    )

    delivery_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="received",
    )

    payload: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
    )