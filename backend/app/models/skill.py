"""Skill — shared skill taxonomy, linked to Profiles and Projects (many-to-many)."""

import uuid

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

profile_skills = Table(
    "profile_skills",
    Base.metadata,
    Column("profile_id", PG_UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", PG_UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True),
)

project_skills = Table(
    "project_skills",
    Base.metadata,
    Column("project_id", PG_UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", PG_UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True),
)


class Skill(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "skills"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)

    profiles: Mapped[list["Profile"]] = relationship(  # noqa: F821
        secondary=profile_skills, back_populates="skills"
    )
    projects: Mapped[list["Project"]] = relationship(  # noqa: F821
        secondary=project_skills, back_populates="skills_required"
    )
