from pydantic import BaseModel, Field


class ProfileCreate(BaseModel):
    full_name: str = Field(min_length=2)
    total_experience: float = Field(ge=0)
    primary_skills: list[str]
    preferred_locations: list[str]
    notice_period_days: int = Field(ge=0)


class ProfileUpdate(BaseModel):
    full_name: str | None = None
    total_experience: float | None = Field(default=None, ge=0)
    primary_skills: list[str] | None = None
    preferred_locations: list[str] | None = None
    notice_period_days: int | None = Field(default=None, ge=0)


class ProfileResponse(ProfileCreate):
    pass