import os
from pathlib import Path
from typesafe_sdk import TypeSafeClient

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def get_llm() -> ChatOpenAI:
    """Cria o modelo configurado para as chamadas ao OpenRouter."""
    arquivo_env = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(arquivo_env)

    return ChatOpenAI(
        model=os.getenv("LLM_MODEL", "openai/gpt-4o-mini"),
        api_key=os.environ["API_KEY"],
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
    )

def get_jev() -> TypeSafeClient:
    """Cria o cliente Jev usando a chave existente do OpenRouter."""
    arquivo_env = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(arquivo_env)

    return TypeSafeClient(
        api_key=os.environ["API_KEY"],
        base_url="https://openrouter.ai/api",
        model="typesafe/jev-1.14",
    )