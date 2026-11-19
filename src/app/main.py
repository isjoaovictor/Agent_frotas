"""Interface Frota Agentic. Execute com python -m streamlit run src/app/main.py."""

import asyncio
import logging
import sys
from base64 import b64encode
from html import escape
from pathlib import Path

import streamlit as st


APP_DIR = Path(__file__).resolve().parent
SRC_DIR = APP_DIR.parent
UTILS_DIR = SRC_DIR / "utils"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

NOME_APP = "Frota Agentic"
ERRO_INTERNO = "Houve um problema interno no servidor da Vale. Tente novamente."
ERRO_VAZIA = "Digite uma pergunta para analisar a frota"
CAMPO_AUSENTE = "Não informado pelo fluxo."
EXTENSOES = (".webp", ".jfif", ".jpg", ".jpeg", ".png")
MIME = {
    ".webp": "image/webp", ".jfif": "image/jpeg", ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg", ".png": "image/png", ".svg": "image/svg+xml",
}
ORIGENS = {
    "relatorio_frota": "Relatório da frota",
    "manual_operacoes": "Manual de operações",
}

# Nome-base da imagem, título, pergunta preenchida e posição do recorte.
ATALHOS = (
    ("navio_1", "Previsão de chegada",
     "Qual navio chega primeiro ao porto?", "50% 50%"),
    ("navio_2", "Reserva de combustível",
     "Algum navio está impedido de zarpar? Qual e por quê?", "50% 50%"),
    ("navio_3", "Velocidade em tempestade",
     "Qual velocidade deve ser usada para o S2-MARE durante a tempestade?", "75% 50%"),
)


# ---------------------------------------------------------------- recursos

@st.cache_resource
def carregar_imagem(base: str, pasta: str = "utils") -> str:
    """Resolve o recurso pelo nome-base e devolve uma data URI. Vazio se ausente."""
    diretorio = UTILS_DIR if pasta == "utils" else APP_DIR
    for extensao in EXTENSOES + (".svg",):
        caminho = diretorio / f"{base}{extensao}"
        if caminho.is_file():
            dados = b64encode(caminho.read_bytes()).decode("ascii")
            return f"data:{MIME[extensao]};base64,{dados}"
    return ""


def img_html(base, classe, pasta="utils", posicao=None):
    uri = carregar_imagem(base, pasta)
    if not uri:
        return f'<div class="{classe} imagem-ausente" aria-hidden="true"></div>'
    estilo = f' style="object-position:{posicao}"' if posicao else ""
    return f'<img class="{classe}" src="{uri}" alt=""{estilo}>'


def executar_script(html):
    """Executa um script curto na página. st.iframe substitui components.html."""
    if hasattr(st, "iframe"):
        st.iframe(html, height=1)
    else:
        import streamlit.components.v1 as components
        components.html(html, height=0)


# ---------------------------------------------------------------- callbacks

def enviar_pergunta():
    """Agenda uma única execução e invalida o resultado da consulta anterior."""
    if st.session_state.processando:
        return
    pergunta = st.session_state.pergunta.strip()
    st.session_state.resultado = None
    st.session_state.erro = ""
    st.session_state.vazia = not pergunta
    if pergunta:
        st.session_state.pergunta_preservada = st.session_state.pergunta
        st.session_state.pergunta_enviada = pergunta
        st.session_state.processando = True


def usar_atalho(pergunta):
    """Preenche o campo antes do rerun, sem iniciar a análise."""
    if st.session_state.processando:
        return
    st.session_state.pergunta = pergunta
    st.session_state.vazia = False
    st.session_state.focar_campo = True


# ---------------------------------------------------------------- conteúdo

def texto_de(conteudo):
    """Extrai texto de conteúdo simples ou de blocos textuais."""
    if isinstance(conteudo, str):
        return conteudo
    if isinstance(conteudo, list):
        partes = []
        for bloco in conteudo:
            if isinstance(bloco, str):
                partes.append(bloco)
            elif isinstance(bloco, dict) and bloco.get("type") == "text":
                partes.append(str(bloco.get("text", "")))
        return "\n".join(partes)
    return str(conteudo)


def reunir_evidencias(resultado):
    """Une contextos, documentos e contextos_regras sem repetições."""
    vistos, grupos = set(), {}
    for campo in ("contextos", "documentos", "contextos_regras"):
        for documento in resultado.get(campo) or []:
            meta = documento.metadata
            chave = (meta.get("doc"), meta.get("secao"), meta.get("posicao"),
                     documento.page_content)
            if chave in vistos:
                continue
            vistos.add(chave)
            origem = ORIGENS.get(meta.get("doc"), str(meta.get("doc") or "Outra origem"))
            grupos.setdefault(origem, []).append(documento)
    return grupos


def mostrar_trecho(documento):
    meta = documento.metadata
    partes = [f'Seção {escape(str(meta.get("secao", CAMPO_AUSENTE)))}']
    if meta.get("posicao") is not None:
        partes.append(f'Posição {escape(str(meta["posicao"]))}')
    st.html(
        '<article class="source">'
        '<p class="source-label">Contexto consultado</p>'
        f'<h4>{escape(str(meta.get("doc", CAMPO_AUSENTE)))}</h4>'
        f'<p class="source-meta">{" · ".join(partes)}</p>'
        f'<blockquote>{escape(documento.page_content)}</blockquote>'
        '</article>'
    )


def mostrar_detalhes(resultado):
    with st.expander("Detalhes da análise"):
        st.markdown("**Pergunta enviada**")
        st.text(st.session_state.pergunta_enviada)
        campos = (
            ("Intenção", resultado.get("intent")),
            ("Identificadores esperados", resultado.get("ids_relatorio")),
            ("Identificadores extraídos",
             [n.get("id") for n in resultado["frota"]] if resultado.get("frota") else None),
            ("Consulta final", resultado.get("consulta_busca")),
            ("Avaliação do contexto", resultado.get("avaliacao")),
            ("Motivo da avaliação", resultado.get("motivo_avaliacao")),
        )
        for rotulo, valor in campos:
            if valor in (None, "", []):
                continue
            st.markdown(f"**{rotulo}**")
            st.text(", ".join(map(str, valor)) if isinstance(valor, list) else str(valor))

        mensagens = resultado.get("messages") or []
        retornos = {
            getattr(m, "tool_call_id", None): texto_de(m.content)
            for m in mensagens if getattr(m, "type", "") == "tool"
        }
        chamadas = [c for m in mensagens for c in (getattr(m, "tool_calls", None) or [])]
        if chamadas:
            st.markdown("**Ferramentas chamadas**")
        for chamada in chamadas:
            st.markdown(f"`{chamada.get('name')}`")
            st.code(str(chamada.get("args")), language="json")
            retorno = retornos.get(chamada.get("id"))
            if retorno is not None:
                st.text(retorno)


def mostrar_resultado(resultado):
    st.html('<h2 class="painel-titulo">Resposta</h2>')
    with st.container(key="resposta_texto"):
        st.markdown(resultado.get("resposta") or resultado.get("resultado")
                    or "O fluxo retornou uma resposta vazia.")

    st.html('<h2 id="evidencias" class="painel-titulo">Evidências</h2>')
    fontes = list(dict.fromkeys(map(str, resultado.get("fontes") or [])))
    if fontes:
        st.caption("Fontes: " + " · ".join(fontes))
    grupos = reunir_evidencias(resultado)
    if not grupos:
        st.caption("Nenhum trecho disponível no resultado.")
    for origem, documentos in grupos.items():
        st.html(f'<h3 class="origem">{escape(origem)}</h3>')
        for documento in documentos:
            mostrar_trecho(documento)
    mostrar_detalhes(resultado)


def cabecalho(tem_resultado):
    evidencias = ('<a href="#evidencias">Evidências</a>' if tem_resultado
                  else '<span class="nav-off" aria-disabled="true">Evidências</span>')
    return (
        '<header class="site-header">'
        '<div class="marca">'
        f'<span class="logo-caixa"><img class="logo-img" src="{carregar_imagem("logo")}" '
        f'alt="Logo {NOME_APP}"></span>'
        f'<span class="marca-nome">{NOME_APP}</span>'
        '</div>'
        f'<nav aria-label="Principal"><a href="#consultar">Consultar</a>{evidencias}</nav>'
        '</header>'
    )


# ---------------------------------------------------------------- execução

async def _executar(pergunta):
    from graph.builder import graph
    from utils.langfuse_client import run_config

    return await graph.ainvoke({"pergunta": pergunta}, config=run_config())


def executar_grafo(pergunta):
    """Ponte síncrona única para o grafo assíncrono."""
    try:
        return asyncio.run(_executar(pergunta))
    finally:
        try:
            from utils.langfuse_client import flush
            flush()
        except Exception:
            logging.getLogger(__name__).warning("Falha ao enviar telemetria", exc_info=True)


def main():
    st.set_page_config(page_title=NOME_APP, page_icon=str(UTILS_DIR / "logo.jpeg"),
                       layout="wide")
    st.html(APP_DIR / "style.css")
    navio = img_html("ship", "navio-svg", pasta="app")

    for chave, valor in {
        "pergunta": "", "pergunta_enviada": "", "pergunta_preservada": "",
        "resultado": None, "processando": False, "erro": "", "vazia": False,
        "focar_campo": False,
        "exibir_resultados": st.session_state.get("resultado") is not None,
    }.items():
        st.session_state.setdefault(chave, valor)

    layout = "results" if st.session_state.exibir_resultados else "initial"
    animar = "true" if st.session_state.pop("animar_resultado", False) else "false"
    tem_resultado = st.session_state.resultado is not None
    st.html(f'<div class="estado" data-layout="{layout}" data-animate="{animar}" hidden></div>')
    st.html(cabecalho(tem_resultado))

    if st.session_state.pop("restaurar_pergunta", False):
        st.session_state.pergunta = st.session_state.pergunta_preservada
    desabilitar = st.session_state.processando

    with st.container(key="abertura"):
        st.html('<span id="consultar"></span>')
        esquerda, direita = st.columns(2, gap="large")
        with esquerda:
            with st.container(key="painel_pergunta"):
                st.title("Consulte sua frota")
                st.caption("Manual e relatório operacional do Porto Alfa")
                with st.form("consulta", clear_on_submit=False, border=False):
                    st.text_area("Sua pergunta", key="pergunta", height=140,
                                 placeholder="Qual navio chega primeiro ao porto?",
                                 disabled=desabilitar)
                    st.form_submit_button("Analisar frota", type="primary",
                                          disabled=desabilitar, on_click=enviar_pergunta)
                if st.session_state.vazia:
                    st.error(ERRO_VAZIA)
                if st.session_state.erro:
                    st.error(st.session_state.erro)
        with direita:
            if tem_resultado:
                with st.container(key="painel_resultado"):
                    mostrar_resultado(st.session_state.resultado)
            else:
                st.html('<figure class="hero-foto">'
                        f'{img_html("navio_1", "hero-img")}</figure>')

    with st.container(key="consultas"):
        st.html('<h2 class="secao-titulo">Consultas rápidas</h2>')
        for coluna, (base, titulo, pergunta, posicao) in zip(st.columns(3, gap="large"), ATALHOS):
            with coluna, st.container(key=f"card_{base}"):
                st.html(f'<div class="card-foto">{img_html(base, "card-img", posicao=posicao)}</div>')
                st.button(titulo, key=f"atalho_{base}", help=pergunta,
                          disabled=desabilitar, on_click=usar_atalho, args=(pergunta,),
                          use_container_width=True)
                st.html(f'<p class="card-pergunta">{escape(pergunta)}</p>')

    if st.session_state.pop("focar_campo", False) or st.session_state.vazia:
        executar_script("""<script>
            const campo = window.parent.document.querySelector('.st-key-pergunta textarea');
            if (campo) {
                campo.focus();
                campo.scrollIntoView({block: 'center'});
            }
        </script>""")

    if st.session_state.processando:
        modal = st.empty()
        modal.markdown(
            '<div class="loading-overlay"><div class="loading-dialog" '
            'role="dialog" aria-modal="true" aria-labelledby="loading-title">'
            f'<div class="orbit" aria-hidden="true"><div class="orbit-ship">{navio}</div></div>'
            '<p id="loading-title" role="status">Gerando resposta</p>'
            '</div></div>', unsafe_allow_html=True,
        )
        try:
            st.session_state.resultado = executar_grafo(st.session_state.pergunta_enviada)
            st.session_state.animar_resultado = not st.session_state.exibir_resultados
            st.session_state.exibir_resultados = True
        except Exception:
            logging.getLogger(__name__).exception("Falha na consulta Frota Agentic")
            st.session_state.resultado = None
            st.session_state.erro = ERRO_INTERNO
        finally:
            st.session_state.processando = False
            st.session_state.restaurar_pergunta = True
            modal.empty()
        st.rerun()


if __name__ == "__main__":
    main()
