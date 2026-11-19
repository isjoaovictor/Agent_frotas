from typing import Literal

from pydantic import BaseModel

from graph.prompts.classify_prompt import CLASSIFY_PROMPT
from graph.state import RAGState
from utils.llm_adapter import get_llm


class Intencao(BaseModel):
    """Restringe a classificação às três intenções do exercício."""

    intent: Literal["regra", "frota", "fora_escopo"]


def classify(state: RAGState) -> dict:
    """Classifica a pergunta e devolve a intenção ao estado."""
    mensagens = CLASSIFY_PROMPT.format_messages(
        pergunta=state["pergunta"]
    )

    modelo = get_llm().with_structured_output(Intencao)
    classificacao = modelo.invoke(mensagens)

    return {"intent": classificacao.intent}