"""Milestone — a payable chunk of a contract, and its uploaded Deliverables."""

import enum
import uuid
from datetime import date

from sqlalchemy import Date, Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class MilestoneStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    REVISION_REQUESTED = "revision_requested"
    APPROVED = "approved"
    PAID = "paid"


class DeliverableStatus(str, enum.Enum):
    SUBMITTED = "submitted"
    REVISION_REQUESTED = "revision_requested"
    APPROVED = "approved"


class Milestone(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "milestones"

    contract_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[MilestoneStatus] = mapped_column(
        Enum(MilestoneStatus, name="milestone_status_enum"), nullable=False, default=MilestoneStatus.PENDING
    )

    contract: Mapped["Contract"] = relationship(back_populates="milestones")  # noqa: F821
    deliverables: Mapped[list["Deliverable"]] = relationship(
        back_populates="milestone", cascade="all, delete-orphan", order_by="Deliverable.created_at"
    )
    invoice: Mapped["Invoice"] = relationship(  # noqa: F821
        back_populates="milestone", uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Milestone id={self.id} title={self.title!r} status={self.status.value}>"


class Deliverable(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "deliverables"

    milestone_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("milestones.id", ondelete="CASCADE"), nullable=False, index=True
    )
    file_url: Mapped[str] = mapped_column(String(500), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[DeliverableStatus] = mapped_column(
        Enum(DeliverableStatus, name="deliverable_status_enum"), nullable=False, default=DeliverableStatus.SUBMITTED
    )

    milestone: Mapped["Milestone"] = relationship(back_populates="deliverables")
