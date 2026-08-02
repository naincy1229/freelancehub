"""
FastAPI dependencies: extract & validate the current user from a JWT,
and enforce role-based access control on protected endpoints.
"""

import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import InvalidTokenError, TokenType, decode_token
from app.db.session import get_db
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository

bearer_scheme = HTTPBearer(auto_error=True)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Decode the access token and load the current user, or raise 401."""
    try:
        payload = decode_token(credentials.credentials, TokenType.ACCESS)
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    user = await UserRepository(db).get_by_id(uuid.UUID(payload["sub"]))
    if user is None or not user.is_active or user.is_suspended:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def require_roles(*allowed_roles: UserRole):
    """Dependency factory: restricts an endpoint to specific roles.

    Usage: `current_user: User = Depends(require_roles(UserRole.CLIENT))`
    """

    async def _check_role(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This action requires one of the following roles: "
                f"{', '.join(r.value for r in allowed_roles)}",
            )
        return current_user

    return _check_role


require_client = require_roles(UserRole.CLIENT)
require_freelancer = require_roles(UserRole.FREELANCER)
require_admin = require_roles(UserRole.ADMIN)
