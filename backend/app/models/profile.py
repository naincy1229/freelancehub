"""
Profile — one-to-one extension of User holding role-specific business data.
Client-only and Freelancer-only fields simply stay null for the other role.
"""

import uuid
from datetime import date

from sqlalchemy import Boolean, Date, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Profile(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    location: Mapped[str | None] = mapped_column(String(150), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # ---------- Freelancer-only fields ----------
    headline: Mapped[str | None] = mapped_column(String(200), nullable=True)
    hourly_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    resume_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    years_experience: Mapped[int | None] = mapped_column(nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    total_earnings: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # ---------- Client-only fields ----------
    company_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    company_website: Mapped[str | None] = mapped_column(String(300), nullable=True)
    total_spent: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # ---------- Shared aggregate rating (denormalized, updated on new review) ----------
    average_rating: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_reviews: Mapped[int] = mapped_column(default=0, nullable=False)

    user: Mapped["User"] = relationship(back_populates="profile")  # noqa: F821
    skills: Mapped[list["Skill"]] = relationship(  # noqa: F821
        secondary="profile_skills", back_populates="profiles"
    )
    education: Mapped[list["Education"]] = relationship(  # noqa: F821
        back_populates="profile", cascade="all, delete-orphan"
    )
    certifications: Mapped[list["Certification"]] = relationship(  # noqa: F821
        back_populates="profile", cascade="all, delete-orphan"
    )
    portfolio_items: Mapped[list["PortfolioItem"]] = relationship(  # noqa: F821
        back_populates="profile", cascade="all, delete-orphan"
    )


class Education(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "education"

    profile_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False
    )
    institution: Mapped[str] = mapped_column(String(200), nullable=False)
    degree: Mapped[str] = mapped_column(String(200), nullable=False)
    field_of_study: Mapped[str | None] = mapped_column(String(200), nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    profile: Mapped["Profile"] = relationship(back_populates="education")


class Certification(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "certifications"

    profile_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    issuing_organization: Mapped[str] = mapped_column(String(200), nullable=False)
    issue_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    credential_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    profile: Mapped["Profile"] = relationship(back_populates="certifications")


class PortfolioItem(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "portfolio_items"

    profile_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    project_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    profile: Mapped["Profile"] = relationship(back_populates="portfolio_items")
