from langchain_core.runnables import RunnableConfig

from graph.state import RAGState
from utils.mcp_client import descobrir_tools


async def tools(state: RAGState, config: RunnableConfig) -> dict:
    """Executa as chamadas solicitadas pela LLM usando o catálogo MCP."""
    ferramentas = await descobrir_tools()

    ferramentas_por_nome = {
        ferramenta.name: ferramenta
        for ferramenta in ferramentas
    }

    solicitacoes = state["messages"][-1].tool_calls
    resultados = []

    for solicitacao in solicitacoes:
        nome = solicitacao["name"]

        if nome not in ferramentas_por_nome:
            raise ValueError(f"Ferramenta ausente no catálogo MCP: {nome}")

        ferramenta = ferramentas_por_nome[nome]
        resultado = await ferramenta.ainvoke(
            solicitacao,
            config=config,
        )

        resultados.append(resultado)

    return {"messages": resultados}