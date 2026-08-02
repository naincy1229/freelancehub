"""Notification — in-app notifications, delivered over WebSocket + persisted here."""

import enum
import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class NotificationType(str, enum.Enum):
    PROPOSAL_RECEIVED = "proposal_received"
    PROPOSAL_ACCEPTED = "proposal_accepted"
    PROPOSAL_REJECTED = "proposal_rejected"
    PROJECT_UPDATED = "project_updated"
    MILESTONE_SUBMITTED = "milestone_submitted"
    MILESTONE_APPROVED = "milestone_approved"
    PAYMENT_RELEASED = "payment_released"
    DEADLINE_REMINDER = "deadline_reminder"
    NEW_MESSAGE = "new_message"
    REVIEW_RECEIVED = "review_received"


class Notification(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "notifications"

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType, name="notification_type_enum"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)

    user: Mapped["User"] = relationship()  # noqa: F821
