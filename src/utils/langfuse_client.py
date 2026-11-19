from pathlib import Path

from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig
from langfuse import get_client
from langfuse.langchain import CallbackHandler


load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def run_config(
    run_name: str = "analise-frota",
    tags: list[str] | None = None,
) -> RunnableConfig:
    """Configura o registro da execução do grafo no Langfuse."""
    return {
        "callbacks": [CallbackHandler()],
        "run_name": run_name,
        "tags": tags or ["agent-frotas"],
        "recursion_limit": 30,
    }


def flush() -> None:
    """Aguarda o envio dos registros pendentes ao Langfuse."""
    get_client().flush()