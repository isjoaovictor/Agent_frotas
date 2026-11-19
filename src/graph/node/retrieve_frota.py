from graph.state import RAGState
from utils.vector_store import DADOS, carregar_chunks


def retrieve_frota(state: RAGState) -> dict:
    """Recupera o relatório completo e identifica os navios que devem ser extraídos."""
    arquivo = DADOS.with_name("relatorio_frota.txt")
    chunks = carregar_chunks(arquivo)

    documentos = [
        chunk
        for chunk in chunks
        if chunk.metadata["doc"] == "relatorio_frota"
    ]

    ids_relatorio = [
        documento.metadata.get("secao", "").strip()
        for documento in documentos
        if documento.metadata.get("secao", "").strip().startswith("S")
        and documento.metadata.get("secao", "").strip().split("-", 1)[0][1:].isdigit()
    ]

    if not ids_relatorio:
        raise ValueError("Nenhuma seção de navio foi identificada no relatório.")

    fontes = [
        f"{documento.metadata['doc']}#{documento.metadata['secao']}"
        for documento in documentos
    ]

    return {
        "documentos": documentos,
        "contextos": documentos,
        "ids_relatorio": ids_relatorio,
        "fontes": fontes,
    }