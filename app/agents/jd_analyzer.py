import logging

from app.integrations.ollama_client import get_llm
from app.modules.jobs.schemas import JobAnalysis

logger = logging.getLogger(__name__)

llm = get_llm().with_structured_output(
    JobAnalysis,
    method="json_schema",
)


async def analyze_jd(description: str) -> JobAnalysis:
    prompt = f"""
    You are a technical recruitment analyst.

    Extract information from this job description.

    JOB DESCRIPTION:
    {description}

    Instructions:

    1. Extract ALL explicitly required technical skills.
    2. Extract preferred or optional skills separately.
    3. Extract minimum years of experience.
    4. Extract responsibilities.
    5. Extract location and work mode.
    6. Do not invent information.
    7. Return a complete structured result.

    Example:

    Job:
    "We need a Python developer with 4+ years of experience.
    FastAPI and React are required. LangGraph is preferred."

    Expected extraction:
    {{
        "required_skills": ["Python", "FastAPI", "React"],
        "preferred_skills": ["LangGraph"],
        "minimum_experience": 4,
        "responsibilities": [],
        "location": null,
        "work_mode": null
    }}
    """

    logger.info("Starting job description analysis (characters=%d)", len(description))
    try:
        result = await llm.ainvoke(prompt)
        analysis = JobAnalysis.model_validate(result)
    except Exception:
        logger.exception("Job description analysis failed")
        raise

    logger.info(
        "Job description analysis completed "
        "(required_skills=%d, preferred_skills=%d, responsibilities=%d, "
        "minimum_experience=%s, location_found=%s, work_mode_found=%s)",
        len(analysis.required_skills),
        len(analysis.preferred_skills),
        len(analysis.responsibilities),
        analysis.minimum_experience,
        analysis.location is not None,
        analysis.work_mode is not None,
    )
    return analysis