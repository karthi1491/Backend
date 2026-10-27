from typing import TypedDict

from app.modules.jobs.schemas import JobAnalysis, ResumeMatchResult


class JDAnalysisState(TypedDict):
    description: str
    analysis: JobAnalysis | None


class ResumeMatchingState(TypedDict):
    description: str
    resume_text: str
    job_analysis: JobAnalysis | None
    match_result: ResumeMatchResult | None