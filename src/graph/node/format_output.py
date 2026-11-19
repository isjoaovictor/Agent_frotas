from graph.state import RAGState


def format_output(state: RAGState) -> dict:
    """Acrescenta as fontes consultadas à resposta sobre regras."""
    fontes = list(dict.fromkeys(state.get("fontes", [])))
    referencias = "\n".join(f"- {fonte}" for fonte in fontes)

    return {
        "resultado": (
            f"{state['resposta']}\n\n"
            f"Fontes consultadas:\n{referencias}"
        )
    }