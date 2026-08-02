"""Project — a client's posted job, and its file attachments."""

import enum
import uuid
from datetime import date

from sqlalchemy import Date, Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.skill import project_skills


class BudgetType(str, enum.Enum):
    FIXED = "fixed"
    HOURLY = "hourly"


class ExperienceLevel(str, enum.Enum):
    ENTRY = "entry"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"


class ProjectStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    CLOSED = "closed"
    COMPLETED = "completed"


class Project(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "projects"

    client_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False
    )

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    budget_type: Mapped[BudgetType] = mapped_column(
        Enum(BudgetType, name="budget_type_enum"), nullable=False, default=BudgetType.FIXED
    )
    budget_min: Mapped[float] = mapped_column(Float, nullable=False)
    budget_max: Mapped[float] = mapped_column(Float, nullable=False)

    experience_level: Mapped[ExperienceLevel] = mapped_column(
        Enum(ExperienceLevel, name="experience_level_enum"), nullable=False, default=ExperienceLevel.INTERMEDIATE
    )
    deadline: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus, name="project_status_enum"), nullable=False, default=ProjectStatus.OPEN, index=True
    )

    client: Mapped["User"] = relationship(foreign_keys=[client_id])  # noqa: F821
    category: Mapped["Category"] = relationship(back_populates="projects")  # noqa: F821
    skills_required: Mapped[list["Skill"]] = relationship(  # noqa: F821
        secondary=project_skills, back_populates="projects"
    )
    attachments: Mapped[list["ProjectAttachment"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    proposals: Mapped[list["Proposal"]] = relationship(  # noqa: F821
        back_populates="project", cascade="all, delete-orphan"
    )
    contract: Mapped["Contract"] = relationship(  # noqa: F821
        back_populates="project", uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Project id={self.id} title={self.title!r} status={self.status.value}>"


class ProjectAttachment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "project_attachments"

    project_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    file_url: Mapped[str] = mapped_column(String(500), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size_bytes: Mapped[int | None] = mapped_column(nullable=True)

    project: Mapped["Project"] = relationship(back_populates="attachments")
