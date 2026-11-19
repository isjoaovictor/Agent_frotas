from graph.state import RAGState


def nao_encontrado(state: RAGState) -> dict:
    """Encerra a consulta quando o manual não sustenta a resposta."""
    mensagem = "Não encontrado no manual de operações."

    return {
        "resposta": mensagem,
        "resultado": mensagem,
    }