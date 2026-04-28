"""Cálculo de indicadores técnicos a partir de séries de preços."""

from __future__ import annotations


def media_movel_simples(precos: list[float], periodo: int) -> float | None:
    if len(precos) < periodo:
        return None
    janela = precos[-periodo:]
    return sum(janela) / periodo


def rsi(precos: list[float], periodo: int = 14) -> float | None:
    if len(precos) <= periodo:
        return None

    ganhos: list[float] = []
    perdas: list[float] = []
    for anterior, atual in zip(precos[-(periodo + 1):-1], precos[-periodo:]):
        variacao = atual - anterior
        if variacao >= 0:
            ganhos.append(variacao)
            perdas.append(0.0)
        else:
            ganhos.append(0.0)
            perdas.append(-variacao)

    media_ganhos = sum(ganhos) / periodo
    media_perdas = sum(perdas) / periodo

    if media_perdas == 0:
        return 100.0
    rs = media_ganhos / media_perdas
    return 100 - (100 / (1 + rs))


def desvio_percentual(preco_atual: float, referencia: float) -> float:
    if referencia == 0:
        return 0.0
    return (preco_atual - referencia) / referencia
