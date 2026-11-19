import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.mcp import MCPAdapter


load_dotenv(Path(__file__).resolve().parents[1] / ".env")


async def descobrir_tools():
    """Descobre e adapta todas as ferramentas publicadas no servidor MCP."""
    endereco = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8000/mcp")

    async with MCPAdapter(endereco) as adapter:
        return await adapter.list_tools()


async def main():
    """Exibe o catálogo descoberto para conferir a conexão MCP."""
    ferramentas = await descobrir_tools()

    for ferramenta in ferramentas:
        print(f"\nNome: {ferramenta.name}")
        print(f"Descrição: {ferramenta.description}")
        print(f"Parâmetros: {ferramenta.args}")


if __name__ == "__main__":
    asyncio.run(main())