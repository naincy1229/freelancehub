"""
Declarative base and shared mixins for all ORM models.

Every model in app/models should inherit from `Base` (and typically
`UUIDPrimaryKeyMixin` + `TimestampMixin` too) so that:
  - all tables get a UUID primary key
  - all tables get created_at / updated_at automatically
  - Alembic can discover every model via this single Base.metadata
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


class UUIDPrimaryKeyMixin:
    """Adds a UUID primary key column named `id`."""

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )


class TimestampMixin:
    """Adds `created_at` and `updated_at` columns, managed by the DB."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
