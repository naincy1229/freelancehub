"""
Centralized application configuration.

All environment-dependent values are loaded here via pydantic-settings.
Never hardcode secrets, URLs, or credentials anywhere else in the codebase —
import `settings` from this module instead.
"""

from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ---------- App ----------
    APP_NAME: str = "FreelanceHub"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    FRONTEND_URL: str = "http://localhost:5173"

    # ---------- Database ----------
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    DATABASE_URL: str
    ASYNC_DATABASE_URL: str

    # ---------- JWT / Security ----------
    JWT_SECRET_KEY: str = Field(..., min_length=32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 30
    EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS: int = 24

    # ---------- Redis / Celery ----------
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # ---------- Email ----------
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 1025
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "no-reply@freelancehub.local"
    SMTP_TLS: bool = False

    # ---------- Google OAuth ----------
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/google/callback"

    # ---------- File Storage ----------
    STORAGE_BACKEND: str = "local"  # "local" | "s3"
    LOCAL_STORAGE_PATH: str = "./storage/uploads"
    MAX_UPLOAD_SIZE_MB: int = 10

    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    AWS_S3_BUCKET: str = "freelancehub-uploads"
    AWS_S3_ENDPOINT_URL: str = ""

    # ---------- Payments ----------
    PAYMENT_GATEWAY: str = "mock"
    PLATFORM_COMMISSION_PERCENT: float = 10.0

    # ---------- Rate limiting ----------
    RATE_LIMIT_PER_MINUTE: int = 60

    # ---------- CORS ----------
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    @field_validator("PLATFORM_COMMISSION_PERCENT")
    @classmethod
    def validate_commission(cls, v: float) -> float:
        if not 0 <= v <= 100:
            raise ValueError("PLATFORM_COMMISSION_PERCENT must be between 0 and 100")
        return v


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance — avoids re-parsing .env on every import."""
    return Settings()


settings = get_settings()
