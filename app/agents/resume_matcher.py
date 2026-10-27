import logging

from app.integrations.ollama_client import get_llm
from app.modules.jobs.schemas import JobAnalysis, ResumeMatchResult

logger = logging.getLogger(__name__)

llm = get_llm().with_structured_output(
    ResumeMatchResult,
    method="json_schema",
)


async def match_resume(
    job_analysis: JobAnalysis,
    resume_text: str,
) -> ResumeMatchResult:

    prompt = f"""
    You are an experienced technical recruiter.

    Compare the candidate's resume with the job requirements.

    JOB REQUIREMENTS:
    {job_analysis.model_dump_json(indent=2)}

    RESUME:
    {resume_text}

    Rules:
    - Identify matching required skills.
    - Identify missing required skills.
    - Identify missing preferred skills.
    - Compare the experience requirement.
    - Provide relevant strengths and recommendations.
    - Calculate a match score between 0 and 100.
    - Do not invent skills or experience.

    Return a complete structured response.
    """

    logger.info(
        "Starting resume match analysis "
        "(resume_characters=%d, required_skills=%d, preferred_skills=%d)",
        len(resume_text),
        len(job_analysis.required_skills),
        len(job_analysis.preferred_skills),
    )
    try:
        result = await llm.ainvoke(prompt)

        # Normalize model output into a Pydantic object.
        match = ResumeMatchResult.model_validate(result)
    except Exception:
        logger.exception("Resume match analysis failed")
        raise

    logger.info(
        "Resume match analysis completed "
        "(score=%d, matched_skills=%d, missing_skills=%d, recommendations=%d)",
        match.match_score,
        len(match.matched_skills),
        len(match.missing_skills),
        len(match.recommendations),
    )
    return match