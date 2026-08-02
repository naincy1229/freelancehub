"""
Aggregates all v1 endpoint routers into a single `api_router`.

Each resource (auth, users, projects, ...) gets its own module in
app/api/v1/endpoints/ and is registered here with its own prefix and tag.
This file is updated incrementally as each endpoint module is built —
nothing is registered here until the corresponding file exists and is complete.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Registered in later steps:
# api_router.include_router(users.router, prefix="/users", tags=["Users"])
# api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
