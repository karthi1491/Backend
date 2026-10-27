from fastapi import HTTPException

from app.modules.jobs.schemas import JobAnalysis, ResumeMatchResult
from app.modules.resume.repository import get_resume
from app.workflows.jd_analysis_graph import jd_analysis_graph
from app.workflows.resume_matching_graph import resume_matching_graph


async def analyze_job(description: str) -> JobAnalysis:
    result = await jd_analysis_graph.ainvoke({
        "description": description,
        "analysis": None,
    })

    return result["analysis"]


async def match_resume(resume_text: str, job_description: str) -> ResumeMatchResult:
    result = await resume_matching_graph.ainvoke({
        "description": job_description,
        "resume_text": resume_text,
        "job_analysis": None,
        "match_result": None,
    })

    return result["match_result"]






async def match_job(description: str):
    resume = await get_resume()

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Please upload your resume first",
        )

    resume_text = resume["content"]

    

    return await match_resume(resume_text, description)


