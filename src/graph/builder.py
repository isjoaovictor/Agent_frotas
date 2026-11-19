from langgraph.graph import END, START, StateGraph

from graph.node.analyze import analyze
from graph.node.extract_frota import extract_frota
from graph.node.format_frota import format_frota
from graph.node.prepare import prepare
from graph.node.retrieve_frota import retrieve_frota
from graph.node.retrieve_regras_calculo import retrieve_regras_calculo
from graph.node.tools import tools
from graph.state import RAGState


def route_after_analyze(state: RAGState) -> str:
    """Continua nas ferramentas ou encaminha a conclusão para formatação."""
    ultima_mensagem = state["messages"][-1]

    if ultima_mensagem.tool_calls:
        return "tools"

    return "format_frota"


builder = StateGraph(RAGState)

builder.add_node("retrieve_frota", retrieve_frota)
builder.add_node("retrieve_regras_calculo", retrieve_regras_calculo)
builder.add_node("extract_frota", extract_frota)
builder.add_node("prepare", prepare)
builder.add_node("analyze", analyze)
builder.add_node("tools", tools)
builder.add_node("format_frota", format_frota)

builder.add_edge(START, "retrieve_frota")
builder.add_edge("retrieve_frota", "retrieve_regras_calculo")
builder.add_edge("retrieve_regras_calculo", "extract_frota")
builder.add_edge("extract_frota", "prepare")
builder.add_edge("prepare", "analyze")

builder.add_conditional_edges(
    "analyze",
    route_after_analyze,
    {
        "tools": "tools",
        "format_frota": "format_frota",
    },
)

builder.add_edge("tools", "analyze")
builder.add_edge("format_frota", END)

graph = builder.compile()