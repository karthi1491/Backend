from fastapi import APIRouter

from app.modules.jobs import service
from app.modules.jobs.schemas import (
    JobAnalyzeRequest,
    JobAnalysis,
    ResumeMatchRequest,
    ResumeMatchResult,
)


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


# Analyze a job description
@router.post("/analyze", response_model=JobAnalysis)
async def analyze_job(request: JobAnalyzeRequest):
    return await service.analyze_job(
        request.description
    )


# Match a job description against the saved resume
@router.post("/match", response_model=ResumeMatchResult)
async def match_job(request: ResumeMatchRequest):
    return await service.match_job(
        request.job_description
    )