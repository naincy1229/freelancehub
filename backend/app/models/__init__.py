"""
Import every model here so that:
  1. `Base.metadata` sees all tables (required for Alembic autogenerate)
  2. SQLAlchemy can resolve string-based relationship() references between models

Import order matters only for readability here -- SQLAlchemy resolves
relationships lazily via the shared registry, not import order.
"""

from app.models.user import User  # noqa: F401
from app.models.profile import Profile, Education, Certification, PortfolioItem  # noqa: F401
from app.models.category import Category  # noqa: F401
from app.models.skill import Skill, profile_skills, project_skills  # noqa: F401
from app.models.project import Project, ProjectAttachment  # noqa: F401
from app.models.proposal import Proposal  # noqa: F401
from app.models.contract import Contract  # noqa: F401
from app.models.milestone import Milestone, Deliverable  # noqa: F401
from app.models.chat import Chat, Message  # noqa: F401
from app.models.notification import Notification  # noqa: F401
from app.models.wallet import Wallet, Transaction  # noqa: F401
from app.models.invoice import Invoice  # noqa: F401
from app.models.review import Review  # noqa: F401
from app.models.report import Report  # noqa: F401
from app.models.admin_log import AdminLog  # noqa: F401

__all__ = [
    "User",
    "Profile",
    "Education",
    "Certification",
    "PortfolioItem",
    "Category",
    "Skill",
    "profile_skills",
    "project_skills",
    "Project",
    "ProjectAttachment",
    "Proposal",
    "Contract",
    "Milestone",
    "Deliverable",
    "Chat",
    "Message",
    "Notification",
    "Wallet",
    "Transaction",
    "Invoice",
    "Review",
    "Report",
    "AdminLog",
]
