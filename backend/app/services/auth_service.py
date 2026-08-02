"""
Auth service — all authentication business logic lives here.

On successful registration this also creates the user's Profile and Wallet
rows in the same transaction, so a User never exists without them.
"""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    TokenType,
    InvalidTokenError,
    create_access_token,
    create_email_verification_token,
    create_password_reset_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.profile import Profile
from app.models.user import User
from app.models.wallet import Wallet
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserLoginRequest, UserRegisterRequest
from app.utils.exceptions import ConflictError, UnauthorizedError, ValidationError


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.users = UserRepository(db)

    async def register(self, data: UserRegisterRequest) -> tuple[User, str, str]:
        """Create a new user + profile + wallet. Returns (user, access_token, refresh_token)."""
        if await self.users.email_exists(data.email):
            raise ConflictError("An account with this email already exists")

        user = User(
            email=data.email.lower(),
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
            role=data.role,
        )
        user = await self.users.create(user)

        # Every user gets a Profile and a Wallet created alongside them.
        self.db.add(Profile(user_id=user.id))
        self.db.add(Wallet(user_id=user.id))
        await self.db.commit()
        await self.db.refresh(user)

        access_token = create_access_token(user.id, user.role.value)
        refresh_token = create_refresh_token(user.id)
        return user, access_token, refresh_token

    async def login(self, data: UserLoginRequest) -> tuple[User, str, str]:
        user = await self.users.get_by_email(data.email.lower())
        if user is None or user.hashed_password is None:
            raise UnauthorizedError("Invalid email or password")
        if not verify_password(data.password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")
        if not user.is_active or user.is_suspended:
            raise UnauthorizedError("This account is disabled. Contact support.")

        access_token = create_access_token(user.id, user.role.value)
        refresh_token = create_refresh_token(user.id)
        return user, access_token, refresh_token

    async def refresh_access_token(self, refresh_token: str) -> str:
        try:
            payload = decode_token(refresh_token, TokenType.REFRESH)
        except InvalidTokenError as exc:
            raise UnauthorizedError("Invalid or expired refresh token") from exc

        user = await self.users.get_by_id(uuid.UUID(payload["sub"]))
        if user is None or not user.is_active or user.is_suspended:
            raise UnauthorizedError("Invalid or expired refresh token")

        return create_access_token(user.id, user.role.value)

    async def request_email_verification(self, user: User) -> str:
        if user.is_email_verified:
            raise ValidationError("Email is already verified")
        return create_email_verification_token(user.id)

    async def verify_email(self, token: str) -> User:
        try:
            payload = decode_token(token, TokenType.EMAIL_VERIFICATION)
        except InvalidTokenError as exc:
            raise UnauthorizedError("Invalid or expired verification link") from exc

        user = await self.users.get_by_id(uuid.UUID(payload["sub"]))
        if user is None:
            raise UnauthorizedError("Invalid or expired verification link")

        user.is_email_verified = True
        await self.users.update(user)
        await self.db.commit()
        return user

    async def request_password_reset(self, email: str) -> str | None:
        """Returns a reset token, or None if no account exists (caller must not leak which)."""
        user = await self.users.get_by_email(email.lower())
        if user is None or user.hashed_password is None:
            return None
        return create_password_reset_token(user.id)

    async def reset_password(self, token: str, new_password: str) -> User:
        try:
            payload = decode_token(token, TokenType.PASSWORD_RESET)
        except InvalidTokenError as exc:
            raise UnauthorizedError("Invalid or expired reset link") from exc

        user = await self.users.get_by_id(uuid.UUID(payload["sub"]))
        if user is None:
            raise UnauthorizedError("Invalid or expired reset link")

        user.hashed_password = hash_password(new_password)
        await self.users.update(user)
        await self.db.commit()
        return user
