"""Lógica de decisão para sinais de compra e venda."""

from __future__ import annotations

from dataclasses import dataclass

import config
from indicadores import desvio_percentual, media_movel_simples, rsi


@dataclass
class Sinal:
    acao: str           # "COMPRAR", "VENDER" ou "AGUARDAR"
    forca: str          # "FORTE", "MODERADO" ou "NEUTRO"
    motivo: str
    preco_atual: float
    sma_curta: float | None
    sma_longa: float | None
    rsi: float | None
    desvio_sma_longa: float


def analisar(preco_atual: float, historico: list[float]) -> Sinal:
    serie = historico + [preco_atual]
    sma_curta = media_movel_simples(serie, config.PERIODO_SMA_CURTA)
    sma_longa = media_movel_simples(serie, config.PERIODO_SMA_LONGA)
    valor_rsi = rsi(serie, config.PERIODO_RSI)
    desvio = desvio_percentual(preco_atual, sma_longa) if sma_longa else 0.0

    if sma_curta is None or sma_longa is None or valor_rsi is None:
        return Sinal(
            acao="AGUARDAR",
            forca="NEUTRO",
            motivo="Histórico insuficiente para análise.",
            preco_atual=preco_atual,
            sma_curta=sma_curta,
            sma_longa=sma_longa,
            rsi=valor_rsi,
            desvio_sma_longa=desvio,
        )

    pontos_compra = 0
    pontos_venda = 0
    motivos: list[str] = []

    if preco_atual < sma_longa:
        pontos_compra += 1
        motivos.append(f"preço {abs(desvio) * 100:.2f}% abaixo da SMA{config.PERIODO_SMA_LONGA}")
    elif preco_atual > sma_longa:
        pontos_venda += 1
        motivos.append(f"preço {desvio * 100:.2f}% acima da SMA{config.PERIODO_SMA_LONGA}")

    if sma_curta < sma_longa:
        pontos_compra += 1
        motivos.append(f"SMA{config.PERIODO_SMA_CURTA} abaixo da SMA{config.PERIODO_SMA_LONGA} (tendência de baixa recente)")
    elif sma_curta > sma_longa:
        pontos_venda += 1
        motivos.append(f"SMA{config.PERIODO_SMA_CURTA} acima da SMA{config.PERIODO_SMA_LONGA} (tendência de alta recente)")

    if valor_rsi <= config.RSI_SOBREVENDIDO:
        pontos_compra += 2
        motivos.append(f"RSI={valor_rsi:.1f} indica sobrevenda")
    elif valor_rsi >= config.RSI_SOBRECOMPRADO:
        pontos_venda += 2
        motivos.append(f"RSI={valor_rsi:.1f} indica sobrecompra")
    else:
        motivos.append(f"RSI={valor_rsi:.1f} em zona neutra")

    if abs(desvio) >= config.DESVIO_FORTE:
        if desvio < 0:
            pontos_compra += 1
        else:
            pontos_venda += 1

    if pontos_compra > pontos_venda and pontos_compra >= 2:
        acao = "COMPRAR"
        forca = "FORTE" if pontos_compra >= 3 else "MODERADO"
    elif pontos_venda > pontos_compra and pontos_venda >= 2:
        acao = "VENDER"
        forca = "FORTE" if pontos_venda >= 3 else "MODERADO"
    else:
        acao = "AGUARDAR"
        forca = "NEUTRO"

    return Sinal(
        acao=acao,
        forca=forca,
        motivo="; ".join(motivos),
        preco_atual=preco_atual,
        sma_curta=sma_curta,
        sma_longa=sma_longa,
        rsi=valor_rsi,
        desvio_sma_longa=desvio,
    )
