from graph.prompts.rag_prompt import RAG_PROMPT
from graph.state import RAGState
from utils.llm_adapter import get_llm


def generate(state: RAGState) -> dict:
    """Gera uma resposta fundamentada nos trechos aprovados do manual."""
    contexto = "\n\n".join(
        f"Seção: {documento.metadata['secao']}\n"
        f"{documento.page_content}"
        for documento in state["contextos"]
    )

    mensagens = RAG_PROMPT.format_messages(
        pergunta=state["pergunta"],
        contexto=contexto,
    )

    resposta = get_llm().invoke(mensagens)

    if not isinstance(resposta.content, str) or not resposta.content.strip():
        raise ValueError("O modelo retornou uma resposta textual vazia ou inesperada.")

    return {"resposta": resposta.content}