from graph.state import RAGState


def format_frota(state: RAGState) -> dict:
    """Disponibiliza a conclusão da análise e suas fontes para apresentação."""
    resposta = state["messages"][-1].content

    if not isinstance(resposta, str) or not resposta.strip():
        raise ValueError("A análise terminou sem uma resposta textual.")

    fontes = list(dict.fromkeys(state.get("fontes", [])))
    referencias = "\n".join(f"- {fonte}" for fonte in fontes)

    return {
        "resposta": resposta,
        "resultado": f"{resposta}\n\nFontes consultadas:\n{referencias}",
    }