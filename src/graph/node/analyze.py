from graph.state import RAGState
from utils.llm_adapter import get_llm
from utils.mcp_client import descobrir_tools


async def analyze(state: RAGState) -> dict:
    """Disponibiliza o catálogo MCP à LLM e solicita o próximo passo da análise."""
    ferramentas = await descobrir_tools()

    if not ferramentas:
        raise RuntimeError("O servidor MCP não disponibilizou ferramentas.")

    modelo = get_llm().bind_tools(ferramentas)
    resposta = await modelo.ainvoke(state["messages"])

    return {"messages": [resposta]}