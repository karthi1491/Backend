from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ResumeResponse(BaseModel):
    filename: str
    content: str
    uploaded_at: datetime


class ResumeOptimizeRequest(BaseModel):
    job_description: str = Field(min_length=30)


class ResumeSuggestion(BaseModel):
    suggestion_id: str

    original_text: str

    suggested_text: str

    reason: str
    decision: Literal["pending", "approve", "reject"] = "pending"


class ResumeOptimizationResult(BaseModel):
    optimization_id: str

    status: Literal["pending", "approved", "rejected"]

    suggestions: list[ResumeSuggestion]

    missing_skills: list[str]

    summary: str


class SuggestionDecision(BaseModel):
    suggestion_id: str

    decision: Literal["approve", "reject"]


class ResumeReviewRequest(BaseModel):
    decisions: list[SuggestionDecision] = Field(min_length=1)



class ResumeVersionResponse(BaseModel):
    version_id: str
    optimization_id: str
    resume_text: str