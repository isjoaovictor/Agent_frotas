import json

from graph.prompts.analyze_prompt import ANALYZE_PROMPT
from graph.state import RAGState


def prepare(state: RAGState) -> dict:
    """Prepara as mensagens de análise com a frota e as regras recuperadas."""
    frota_json = json.dumps(state["frota"], ensure_ascii=False)

    mensagens = ANALYZE_PROMPT.format_messages(
        regras=state["contexto_regras"],
        frota=frota_json,
        pergunta=state["pergunta"],
    )

    return {"messages": mensagens}