from pydantic import BaseModel

from graph.prompts.grade_prompt import GRADE_PROMPT
from graph.state import RAGState
from utils.llm_adapter import get_llm


class AvaliacaoRegras(BaseModel):
    """Representa se o contexto sustenta uma resposta à pergunta."""

    suficiente: bool


def grade(state: RAGState) -> dict:
    """Avalia a suficiência dos trechos recuperados do manual."""
    documentos = state["contextos"]

    if not documentos:
        return {"suficiente": False}

    contexto = "\n\n".join(
        documento.page_content
        for documento in documentos
    )

    mensagens = GRADE_PROMPT.format_messages(
        pergunta=state["pergunta"],
        contexto=contexto,
    )

    modelo = get_llm().with_structured_output(
        AvaliacaoRegras,
        method="function_calling",
    )
    avaliacao = modelo.invoke(mensagens)

    return {"suficiente": avaliacao.suficiente}