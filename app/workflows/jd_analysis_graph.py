from langgraph.graph import StateGraph, START, END

from app.agents.jd_analyzer import analyze_jd
from app.workflows.state import JDAnalysisState


async def jd_analyzer_node(state: JDAnalysisState):
    result = await analyze_jd(state["description"])

    return {
        "analysis": result,
    }


graph_builder = StateGraph(JDAnalysisState)

graph_builder.add_node(
    "jd_analyzer",
    jd_analyzer_node,
)

graph_builder.add_edge(START, "jd_analyzer")
graph_builder.add_edge("jd_analyzer", END)

jd_analysis_graph = graph_builder.compile()