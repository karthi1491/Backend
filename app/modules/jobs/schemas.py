from pydantic import BaseModel, Field


class JobAnalyzeRequest(BaseModel):
    description: str = Field(min_length=30)


class ResumeMatchRequest(BaseModel):
    job_description: str = Field(min_length=30)


class JobAnalysis(BaseModel):
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    minimum_experience: float | None = None
    responsibilities: list[str] = Field(default_factory=list)
    location: str | None = None
    work_mode: str | None = None


# class ResumeMatchResult(BaseModel):
#     matched_skills: list[str] = Field(default_factory=list)
#     missing_skills: list[str] = Field(default_factory=list)
#     match_score: float = 0.0
#     summary: str | None = None


class ResumeMatchResult(BaseModel):

    match_score: int = Field(ge=0, le=100)

    matched_skills: list[str]

    missing_skills: list[str]

    preferred_skills_missing: list[str]

    experience_match: bool | None

    strengths: list[str]

    recommendations: list[str]