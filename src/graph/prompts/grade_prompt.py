from langchain_core.prompts import ChatPromptTemplate


GRADE_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "Verifique se o contexto fornecido contém as informações "
        "necessárias para responder à pergunta.\n"
        "Marque suficiente=true somente quando houver suporte explícito "
        "para a resposta.\n"
        "Um trecho relacionado ao assunto pode ser insuficiente.\n"
        "Não use conhecimento externo nem adapte regras de uma condição "
        "para outra. Limites de tempestade não estabelecem limites "
        "para nevoeiro.\n"
        "Quando faltar informação necessária, marque suficiente=false."
    ),
    (
        "human",
        "Pergunta: {pergunta}\n\n"
        "Contexto recuperado:\n{contexto}"
    ),
])