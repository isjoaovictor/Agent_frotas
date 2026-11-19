import math

from fastmcp import FastMCP


mcp = FastMCP("Agent_frotas")


@mcp.tool
def reserva_ok(combustivel_t: float, reserva_t: float) -> bool:
    """Função: Verifica se o combustível a bordo cobre a reserva mínima.

    Recebe combustível e reserva em toneladas.
    Retorna True quando o combustível é maior ou igual à reserva.
    Retorna False quando a reserva mínima não está atendida.
    """
    if not all(math.isfinite(v) and v >= 0 for v in (combustivel_t, reserva_t)):
        raise ValueError("Combustível e reserva devem ser finitos e não negativos.")

    return combustivel_t >= reserva_t


@mcp.tool
def velocidade_efetiva(
    velocidade_kn: float,
    em_tempestade: bool,
    limite_tempestade_kn: float,
) -> float:
    """Determina a velocidade em nós usada para estimar a viagem.

    Recebe a velocidade planejada, a presença de tempestade e o limite
    recuperado do manual para a rota do navio.
    Em tempestade, retorna o menor valor entre velocidade e limite.
    Sem tempestade, retorna a velocidade planejada.
    """
    valores = (velocidade_kn, limite_tempestade_kn)
    if not all(math.isfinite(v) and v >= 0 for v in valores):
        raise ValueError("Velocidade e limite devem ser finitos e não negativos.")

    return min(velocidade_kn, limite_tempestade_kn) if em_tempestade else velocidade_kn


@mcp.tool
def calcular_eta_horas(distancia_nm: float, velocidade_kn: float) -> float:
    """Função: Calcula o tempo estimado de viagem em horas.

    Recebe distância em milhas náuticas e velocidade efetiva em nós.
    A distância deve ser não negativa e a velocidade deve ser positiva.
    Retorna distância dividida pela velocidade, arredondada a duas casas.
    """
    if not math.isfinite(distancia_nm) or distancia_nm < 0:
        raise ValueError("A distância deve ser finita e não negativa.")

    if not math.isfinite(velocidade_kn) or velocidade_kn <= 0:
        raise ValueError("O ETA exige velocidade finita e maior que zero.")

    return round(distancia_nm / velocidade_kn, 2)


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)