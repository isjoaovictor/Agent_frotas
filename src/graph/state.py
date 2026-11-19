from typing import TypedDict, Literal, Annotated
from langchain_core.documents import Document
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
import operator

class RAGState(TypedDict, total=False):
    """Armazena as informações compartilhadas pelos nós do RAG."""

    pergunta: str
    consulta_busca: str
    tentativas_busca: int

    documentos: list[Document]
    contextos: list[Document]
    intent_confidence: float
    intent_probabilities: dict[str, float]
    suficiente: bool

    expandido: bool
    decisao: str

    resposta: str
    fontes: Annotated[list[str], operator.add]
    avaliacao: str
    motivo_avaliacao: str
    intent: Literal["regra", "frota", "fora_escopo"]  #intenção
    messages: Annotated[list[AnyMessage], add_messages]
    ids_relatorio: list[str]
    frota: list[dict]
    contexto_regras: str
    contextos_regras: list[Document]
