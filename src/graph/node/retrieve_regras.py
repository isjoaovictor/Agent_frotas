from graph.state import RAGState
from utils.vector_store import buscar_hibrida


def retrieve_regras(state: RAGState) -> dict:
    """Recupera trechos do manual relacionados à pergunta do operador."""
    documentos = buscar_hibrida(
        pergunta=state["pergunta"],
        k=3,
        doc="manual_operacoes",
    )

    return {
        "contextos": documentos,
        "fontes": [
            f"{documento.metadata['doc']}#{documento.metadata['secao']}"
            for documento in documentos
        ],
    }