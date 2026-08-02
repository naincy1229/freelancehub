"""Contract — created when a client hires a freelancer for a project."""

import enum
import uuid

from sqlalchemy import Enum, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class ContractStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    TERMINATED = "terminated"


class Contract(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "contracts"

    project_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    proposal_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("proposals.id"), unique=True, nullable=False
    )
    client_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    freelancer_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[ContractStatus] = mapped_column(
        Enum(ContractStatus, name="contract_status_enum"), nullable=False, default=ContractStatus.ACTIVE, index=True
    )

    project: Mapped["Project"] = relationship(back_populates="contract")  # noqa: F821
    proposal: Mapped["Proposal"] = relationship()  # noqa: F821
    client: Mapped["User"] = relationship(foreign_keys=[client_id])  # noqa: F821
    freelancer: Mapped["User"] = relationship(foreign_keys=[freelancer_id])  # noqa: F821

    milestones: Mapped[list["Milestone"]] = relationship(  # noqa: F821
        back_populates="contract", cascade="all, delete-orphan", order_by="Milestone.created_at"
    )
    chat: Mapped["Chat"] = relationship(  # noqa: F821
        back_populates="contract", uselist=False, cascade="all, delete-orphan"
    )
    reviews: Mapped[list["Review"]] = relationship(  # noqa: F821
        back_populates="contract", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Contract id={self.id} project_id={self.project_id} status={self.status.value}>"
