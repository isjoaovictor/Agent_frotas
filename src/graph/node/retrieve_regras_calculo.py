from graph.state import RAGState
from utils.vector_store import buscar_hibrida


CONSULTA = (
    "velocidade segura em tempestade por rota, "
    "reserva mínima de combustível e cálculo do tempo de viagem ETA"
)


def retrieve_regras_calculo(state: RAGState) -> dict:
    """Recupera as regras do manual necessárias à análise da frota."""
    documentos = buscar_hibrida(
        pergunta=CONSULTA,
        k=4,
        doc="manual_operacoes",
    )

    contexto = "\n\n".join(
        f"Documento: {documento.metadata['doc']}\n"
        f"Seção: {documento.metadata['secao']}\n"
        f"{documento.page_content}"
        for documento in documentos
    )

    fontes = [
        f"{documento.metadata['doc']}#{documento.metadata['secao']}"
        for documento in documentos
    ]

    return {
        "contexto_regras": contexto,
        "contextos_regras": documentos,
        "fontes": fontes,
    }