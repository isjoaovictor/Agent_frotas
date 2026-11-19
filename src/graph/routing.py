from graph.state import RAGState


def route_by_intent(state: RAGState) -> str:
    """Retorna a intenção escolhida para selecionar o próximo caminho."""
    return state["intent"]

def route_after_grade(state: RAGState) -> str:
    """Escolhe entre gerar a resposta e encerrar por falta de informação."""
    return "suficiente" if state["suficiente"] else "insuficiente"

def route_after_analyze(state: RAGState) -> str:
    """Encaminha solicitações às ferramentas ou finaliza a análise."""
    if state["messages"][-1].tool_calls:
        return "tools"

    return "format_frota"