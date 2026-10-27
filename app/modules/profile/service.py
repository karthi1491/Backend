from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

from app.modules.profile import repository
from app.modules.profile.schemas import (
    ProfileCreate,
    ProfileUpdate,
)


async def create_profile(profile: ProfileCreate):
    try:
        await repository.create_profile(
            profile.model_dump()
        )
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="Profile already exists",
        )

    return await repository.get_profile()


async def get_profile():
    profile = await repository.get_profile()

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    return profile


async def update_profile(profile: ProfileUpdate):
    updates = profile.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(
            status_code=400,
            detail="No fields provided",
        )

    updated = await repository.update_profile(updates)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    return await repository.get_profile()