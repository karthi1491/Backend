import logging

from langgraph.graph import END, START, StateGraph

from app.agents.jd_analyzer import analyze_jd
from app.agents.resume_matcher import match_resume
from app.workflows.state import ResumeMatchingState

logger = logging.getLogger(__name__)


async def jd_analyzer_node(state: ResumeMatchingState):
    logger.info("Resume matching workflow: analyzing job description")
    analysis = await analyze_jd(
        state["description"]
    )

    if not analysis.required_skills:
        raise ValueError(
            "JD Analyzer returned no required skills"
        )

    return {
        "job_analysis": analysis
    }

async def resume_matcher_node(state: ResumeMatchingState):
    logger.info("Resume matching workflow: comparing resume to job requirements")
    result = await match_resume(
        job_analysis=state["job_analysis"],
        resume_text=state["resume_text"],
    )

    return {
        "match_result": result
    }


builder = StateGraph(ResumeMatchingState)

builder.add_node(
    "jd_analyzer",
    jd_analyzer_node,
)

builder.add_node(
    "resume_matcher",
    resume_matcher_node,
)

builder.add_edge(START, "jd_analyzer")
builder.add_edge("jd_analyzer", "resume_matcher")
builder.add_edge("resume_matcher", END)

resume_matching_graph = builder.compile()