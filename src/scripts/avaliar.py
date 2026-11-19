import asyncio
import json
from pathlib import Path

from graph.builder import graph
from utils.langfuse_client import flush, run_config

from langfuse import get_client


DADOS = Path(__file__).resolve().parents[1] / "dados"


async def main():
    """Avalia as perguntas do gabarito e registra um score por execução."""
    casos = json.loads(
        (DADOS / "avaliacao.json").read_text(encoding="utf-8-sig")
    )

    langfuse = get_client()
    acertos = 0

    try:
        for caso in casos:
            identificador = caso["id"]
            esperados = caso["esperado"]

            with langfuse.start_as_current_observation(
                as_type="span",
                name=f"avaliacao-{identificador}",
            ) as observacao:
                observacao.update(
                    input={
                        "pergunta": caso["pergunta"],
                        "termos_esperados": esperados,
                    }
                )

                try:
                    saida = await graph.ainvoke(
                        {"pergunta": caso["pergunta"]},
                        config=run_config(
                            run_name=f"grafo-{identificador}",
                            tags=["avaliacao", "etapa-2"],
                        ),
                    )

                    texto = saida.get("resposta") or saida.get("resultado", "")
                    ausentes = [
                        termo
                        for termo in esperados
                        if termo.casefold() not in texto.casefold()
                    ]

                    aprovado = bool(texto.strip()) and not ausentes

                    observacao.update(
                        output={
                            "resposta": texto,
                            "intent": saida.get("intent"),
                            "termos_ausentes": ausentes,
                        }
                    )

                    comentario = (
                        f"Termos ausentes: {ausentes}"
                        if ausentes
                        else "Todos os termos esperados foram encontrados."
                    )

                    if not texto.strip():
                        comentario = "O fluxo terminou sem resposta textual."

                except Exception as erro:
                    aprovado = False
                    comentario = f"{type(erro).__name__}: {erro}"

                    observacao.update(
                        output={"erro": comentario},
                        level="ERROR",
                        status_message=comentario,
                    )

                observacao.score_trace(
                    name="gabarito",
                    value=1.0 if aprovado else 0.0,
                    data_type="BOOLEAN",
                    comment=comentario,
                )

                acertos += int(aprovado)
                print(
                    identificador,
                    "OK" if aprovado else "FALHOU",
                    "" if aprovado else comentario,
                )

        total = len(casos)
        percentual = acertos / total * 100 if total else 0

        print(f"\nAcertos: {acertos}/{total} ({percentual:.1f}%)")

    finally:
        flush()


if __name__ == "__main__":
    asyncio.run(main())