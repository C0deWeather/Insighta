from fastapi import Request, Depends
from typing import Annotated
from app.db import Database
from app.repositories import ProfileRepo


async def get_db(request: Request) -> Database:
    """Dependency to get the database instance from the app state."""
    return request.app.state.db


async def get_profile_repo(db: Annotated[Database, Depends(get_db)]) -> ProfileRepo:
    """Dependency to get the profile repository."""
    return ProfileRepo(db)
