from graph.state import RAGState


def refuse(state: RAGState) -> dict:
    """Encerra perguntas classificadas fora do domínio da aplicação."""
    mensagem = "Pergunta fora do escopo (navios, portos e regras de operação)."

    return {
        "resposta": mensagem,
        "resultado": mensagem,
    }