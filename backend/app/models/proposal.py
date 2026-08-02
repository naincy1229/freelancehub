"""Proposal — a freelancer's bid on a project."""

import enum
import uuid

from sqlalchemy import Enum, Float, ForeignKey, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class ProposalStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class Proposal(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "proposals"
    __table_args__ = (
        UniqueConstraint("project_id", "freelancer_id", name="uq_one_proposal_per_freelancer_per_project"),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    freelancer_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    cover_letter: Mapped[str] = mapped_column(Text, nullable=False)
    bid_amount: Mapped[float] = mapped_column(Float, nullable=False)
    estimated_days: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[ProposalStatus] = mapped_column(
        Enum(ProposalStatus, name="proposal_status_enum"), nullable=False, default=ProposalStatus.PENDING, index=True
    )

    project: Mapped["Project"] = relationship(back_populates="proposals")  # noqa: F821
    freelancer: Mapped["User"] = relationship(foreign_keys=[freelancer_id])  # noqa: F821

    def __repr__(self) -> str:
        return f"<Proposal id={self.id} project_id={self.project_id} status={self.status.value}>"
