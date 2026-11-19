from langchain_core.prompts import ChatPromptTemplate


RAG_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "Responda à pergunta usando exclusivamente o contexto fornecido.\n"
        "Preserve números, unidades e condições das regras.\n"
        "Identifique a seção que fundamenta a resposta.\n"
        "Não use conhecimento externo nem invente informações.\n"
        "Se o contexto não sustentar a resposta, responda exatamente:\n"
        "Não encontrado no manual de operações."
    ),
    (
        "human",
        "Pergunta: {pergunta}\n\n"
        "Contexto:\n{contexto}"
    ),
])