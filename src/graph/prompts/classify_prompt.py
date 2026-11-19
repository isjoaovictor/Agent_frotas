from langchain_core.prompts import ChatPromptTemplate


CLASSIFY_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "Atue como um especialista em classificação de filtros de RAG e de perguntas de operadores de porto.\n"
        "Classifique a pergunta de um operador de porto.\n"
        "regra: pergunta sobre regras, limites e procedimentos gerais "
        "do manual de operações.\n"
        "frota: pergunta que depende da situação atual dos navios, "
        "como combustível disponível, impedimento de partida, "
        "velocidade efetiva, ETA ou comparação entre navios.\n"
        "fora_escopo: pergunta sem relação com operações marítimas "
        "ou com a frota.\n"
        "Uma pergunta sobre navegação cuja resposta talvez esteja "
        "ausente no manual continua sendo regra.\n"
        "Exemplos:\n"
        "Qual a reserva mínima de combustível? -> regra\n"
        "O S1-FAROL tem combustível suficiente para zarpar? -> frota\n"
        "Qual a velocidade máxima em nevoeiro? -> regra\n"
        "Qual navio chega primeiro? -> frota\n"
        "Qual a capital do Brasil? -> fora_escopo"
    ),
    (
        "human",
        "{pergunta}"
    ),
])