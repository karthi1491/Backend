from fastapi import APIRouter, status

from app.modules.profile import service
from app.modules.profile.schemas import (
    ProfileCreate,
    ProfileUpdate,
    ProfileResponse,
)


router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
)


@router.post(
    "",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_profile(profile: ProfileCreate):
    return await service.create_profile(profile)


@router.get("", response_model=ProfileResponse)
async def get_profile():
    return await service.get_profile()


@router.patch("", response_model=ProfileResponse)
async def update_profile(profile: ProfileUpdate):
    return await service.update_profile(profile)