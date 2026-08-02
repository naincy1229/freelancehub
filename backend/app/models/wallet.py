"""Wallet (one per user) and Transaction (immutable ledger entries)."""

import enum
import uuid

from sqlalchemy import Enum, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class TransactionType(str, enum.Enum):
    DEPOSIT = "deposit"              # client adds funds to wallet
    ESCROW_HOLD = "escrow_hold"      # funds moved into escrow for a milestone
    ESCROW_RELEASE = "escrow_release"  # escrow released to freelancer on approval
    WITHDRAWAL = "withdrawal"        # freelancer withdraws earnings
    REFUND = "refund"                # escrow refunded to client
    COMMISSION = "commission"        # platform commission deducted


class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Wallet(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "wallets"

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    balance: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    escrow_balance: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)

    user: Mapped["User"] = relationship(back_populates="wallet")  # noqa: F821
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="wallet", cascade="all, delete-orphan", order_by="Transaction.created_at.desc()"
    )


class Transaction(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "transactions"

    wallet_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    milestone_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("milestones.id"), nullable=True
    )
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType, name="transaction_type_enum"), nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus, name="transaction_status_enum"), nullable=False, default=TransactionStatus.PENDING
    )
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str | None] = mapped_column(String(300), nullable=True)
    reference_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    wallet: Mapped["Wallet"] = relationship(back_populates="transactions")
    milestone: Mapped["Milestone"] = relationship()  # noqa: F821
