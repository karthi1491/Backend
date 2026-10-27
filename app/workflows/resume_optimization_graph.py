from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.agents.resume_optimizer import (
    AIOptimizationOutput,
    optimize_resume,
)


class ResumeOptimizationState(TypedDict):
    resume_text: str
    job_description: str
    optimization_result: AIOptimizationOutput | None


async def optimizer_node(state: ResumeOptimizationState):

    result = await optimize_resume(
        resume_text=state["resume_text"],
        job_description=state["job_description"],
    )

    return {
        "optimization_result": result
    }


builder = StateGraph(ResumeOptimizationState)

builder.add_node(
    "resume_optimizer",
    optimizer_node,
)

builder.add_edge(START, "resume_optimizer")
builder.add_edge("resume_optimizer", END)

resume_optimization_graph = builder.compile()