from typesafe_sdk import Choice

from graph.state import RAGState
from utils.llm_adapter import get_jev


def classify(state: RAGState) -> dict:
    """Classifica a pergunta com Jev e registra a confiança da decisão."""
    pergunta = state["pergunta"].strip()

    if not pergunta:
        raise ValueError("A pergunta não pode estar vazia.")

    with get_jev() as cliente:
        resposta = cliente.system_one(
            state=pergunta,
            questions={
                "intent": Choice(
                    instructions=(
                        "Classifique a pergunta de um operador do Porto Alfa. "
                        "O domínio inclui navios, rotas, velocidades, tempestades, "
                        "combustível, abastecimento, falhas de motor, reparos, "
                        "custos operacionais, descarga e prazos. "
                        "Interprete perguntas curtas nesse contexto marítimo, "
                        "mesmo quando não mencionarem explicitamente navio ou porto. "
                        "Diferencie uma regra geral da situação atual dos navios. "
                        "Perguntas sobre condições não documentadas, como nevoeiro, "
                        "continuam sendo regra."
                    ),
                    criteria={
                        "regra": (
                            "Pergunta sobre regras, limites, preços, custos, durações "
                            "ou procedimentos gerais das operações marítimas. "
                            "Inclui reserva mínima, abastecimento, reparo de motor, "
                            "descarga e prazos previstos no manual. "
                            "Exemplos: quanto custa o reparo do motor, quanto tempo "
                            "dura a descarga e qual o limite de velocidade."
                        ),
                        "frota": (
                            "Pergunta que depende da situação dos navios "
                            "no relatório, incluindo combustível disponível, "
                            "impedimento de partida, velocidade efetiva, "
                            "ETA ou comparação entre navios."
                        ),
                        "fora_escopo": (
                            "Pergunta sem relação com operações marítimas "
                            "ou com a frota."
                        ),
                    },
                ),
            },
        )

    classificacao = resposta.answers["intent"]

    return {
        "intent": classificacao.choice,
        "intent_confidence": classificacao.confidence,
        "intent_probabilities": classificacao.probabilities,
    }