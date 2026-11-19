from langchain_core.prompts import ChatPromptTemplate


EXTRACT_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "Extraia todos os navios do relatório fornecido.\n"
        "Copie os identificadores e os valores exatamente como aparecem.\n"
        "Não faça cálculos, não aplique regras e não altere velocidades.\n"
        "A velocidade extraída é a velocidade-alvo planejada do relatório.\n"
        "Converta tempestade 'sim' para true e 'não' para false.\n"
        "Ignore a seção 'Sobre este documento' na lista de navios.\n"
        "Não invente dados ausentes."
    ),
    (
        "human",
        "{relatorio}"
    ),
])