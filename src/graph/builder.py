from langgraph.graph import END, START, StateGraph

from graph.node.analyze import analyze
from graph.node.classify import classify
from graph.node.extract_frota import extract_frota
from graph.node.format_frota import format_frota
from graph.node.format_output import format_output
from graph.node.generate import generate
from graph.node.grade import grade
from graph.node.nao_encontrado import nao_encontrado
from graph.node.prepare import prepare
from graph.node.refuse import refuse
from graph.node.retrieve_frota import retrieve_frota
from graph.node.retrieve_regras import retrieve_regras
from graph.node.retrieve_regras_calculo import retrieve_regras_calculo
from graph.node.tools import tools
from graph.routing import (
    route_after_analyze,
    route_after_grade,
    route_by_intent,
)
from graph.state import RAGState


builder = StateGraph(RAGState)

nos = {
    "classify": classify,
    "retrieve_regras": retrieve_regras,
    "grade": grade,
    "generate": generate,
    "format_output": format_output,
    "nao_encontrado": nao_encontrado,
    "refuse": refuse,
    "retrieve_frota": retrieve_frota,
    "retrieve_regras_calculo": retrieve_regras_calculo,
    "extract_frota": extract_frota,
    "prepare": prepare,
    "analyze": analyze,
    "tools": tools,
    "format_frota": format_frota,
}

for nome, funcao in nos.items():
    builder.add_node(nome, funcao)

builder.add_edge(START, "classify")

builder.add_conditional_edges(
    "classify",
    route_by_intent,
    {
        "regra": "retrieve_regras",
        "frota": "retrieve_frota",
        "fora_escopo": "refuse",
    },
)

builder.add_edge("retrieve_regras", "grade")

builder.add_conditional_edges(
    "grade",
    route_after_grade,
    {
        "suficiente": "generate",
        "insuficiente": "nao_encontrado",
    },
)

builder.add_edge("generate", "format_output")

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

for terminal in (
    "format_output",
    "nao_encontrado",
    "refuse",
    "format_frota",
):
    builder.add_edge(terminal, END)

graph = builder.compile()