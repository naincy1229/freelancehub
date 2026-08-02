"""
Domain-level exceptions.

Services raise these instead of FastAPI's HTTPException directly, so business
logic stays framework-agnostic and testable. The API layer (endpoints) catches
these and maps them to the correct HTTP status code.
"""


class AppError(Exception):
    """Base class for all domain exceptions."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(AppError):
    """Requested resource does not exist."""


class ConflictError(AppError):
    """Resource already exists / violates a uniqueness constraint."""


class UnauthorizedError(AppError):
    """Authentication failed or credentials are invalid."""


class ForbiddenError(AppError):
    """Authenticated but not allowed to perform this action."""


class ValidationError(AppError):
    """Input is well-formed but fails a business rule."""
