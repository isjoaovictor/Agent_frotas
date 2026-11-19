from collections import Counter

from pydantic import BaseModel, Field

from graph.prompts.extract_prompt import EXTRACT_PROMPT
from graph.state import RAGState
from utils.llm_adapter import get_llm


class NavioRelatorio(BaseModel):
    """Representa os dados originais de um navio descrito no relatório."""

    id: str
    destino: str
    distancia_nm: float = Field(ge=0)
    velocidade_kn: float = Field(ge=0)
    combustivel_t: float = Field(ge=0)
    reserva_t: float = Field(ge=0)
    em_tempestade: bool


class FrotaRelatorio(BaseModel):
    """Agrupa todos os navios extraídos do relatório."""

    navios: list[NavioRelatorio]


def extract_frota(state: RAGState) -> dict:
    """Extrai os navios e verifica omissões, duplicações e identificadores extras."""
    relatorio = "\n\n".join(
        documento.page_content
        for documento in state["contextos"]
    )

    mensagens = EXTRACT_PROMPT.format_messages(relatorio=relatorio)

    modelo = get_llm().with_structured_output(
        FrotaRelatorio,
        method="function_calling",
    )
    extracao = modelo.invoke(mensagens)

    esperados = Counter(state["ids_relatorio"])
    encontrados = Counter(navio.id for navio in extracao.navios)

    if encontrados != esperados:
        raise ValueError(
            "A extração divergiu dos navios presentes no relatório. "
            f"Esperados: {dict(esperados)}. "
            f"Encontrados: {dict(encontrados)}."
        )

    return {
        "frota": [
            navio.model_dump()
            for navio in extracao.navios
        ]
    }