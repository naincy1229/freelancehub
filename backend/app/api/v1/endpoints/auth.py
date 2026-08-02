"""Authentication endpoints: register, login, refresh, email verification, password reset."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import (
    AuthResponse,
    ForgotPasswordRequest,
    RefreshTokenRequest,
    ResetPasswordRequest,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
    VerifyEmailRequest,
)
from app.services.auth_service import AuthService
from app.utils.exceptions import ConflictError, UnauthorizedError

router = APIRouter()


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(data: UserRegisterRequest, db: AsyncSession = Depends(get_db)) -> AuthResponse:
    """Register a new Client or Freelancer account. Admin accounts cannot self-register."""
    service = AuthService(db)
    try:
        user, access_token, refresh_token = await service.register(data)
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message) from exc

    return AuthResponse(
        user=UserResponse.model_validate(user),
        tokens=TokenResponse(access_token=access_token, refresh_token=refresh_token),
    )


@router.post("/login", response_model=AuthResponse)
async def login(data: UserLoginRequest, db: AsyncSession = Depends(get_db)) -> AuthResponse:
    service = AuthService(db)
    try:
        user, access_token, refresh_token = await service.login(data)
    except UnauthorizedError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=exc.message) from exc

    return AuthResponse(
        user=UserResponse.model_validate(user),
        tokens=TokenResponse(access_token=access_token, refresh_token=refresh_token),
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    """Exchange a valid refresh token for a new short-lived access token."""
    service = AuthService(db)
    try:
        access_token = await service.refresh_access_token(data.refresh_token)
    except UnauthorizedError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=exc.message) from exc

    return TokenResponse(access_token=access_token, refresh_token=data.refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(current_user: User = Depends(get_current_user)) -> None:
    """
    Stateless JWT logout: the client discards its tokens. Since access tokens
    are short-lived, no server-side blacklist is required for this MVP; a
    Redis-backed blacklist can be added later if immediate revocation is needed.
    """
    return None


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(current_user)


@router.post("/verify-email", response_model=UserResponse)
async def verify_email(data: VerifyEmailRequest, db: AsyncSession = Depends(get_db)) -> UserResponse:
    service = AuthService(db)
    try:
        user = await service.verify_email(data.token)
    except UnauthorizedError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=exc.message) from exc
    return UserResponse.model_validate(user)


@router.post("/forgot-password", status_code=status.HTTP_202_ACCEPTED)
async def forgot_password(data: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """
    Always returns a generic success message, whether or not the email exists,
    to avoid leaking which emails are registered. The reset token (when a user
    does exist) is dispatched via the email task queue, not returned here.
    """
    service = AuthService(db)
    token = await service.request_password_reset(data.email)
    if token is not None:
        # In a later step this is handed to a Celery task that emails the link:
        # send_password_reset_email.delay(data.email, token)
        pass
    return {"message": "If an account with that email exists, a password reset link has been sent."}


@router.post("/reset-password", response_model=UserResponse)
async def reset_password(data: ResetPasswordRequest, db: AsyncSession = Depends(get_db)) -> UserResponse:
    service = AuthService(db)
    try:
        user = await service.reset_password(data.token, data.new_password)
    except UnauthorizedError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=exc.message) from exc
    return UserResponse.model_validate(user)
