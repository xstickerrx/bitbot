"""Cliente HTTP para a API pública da CoinGecko."""

from __future__ import annotations

import requests

import config


class ErroAPI(Exception):
    pass


def obter_preco_atual(moeda: str = config.MOEDA_FIAT) -> float:
    parametros = {"ids": "bitcoin", "vs_currencies": moeda}
    try:
        resposta = requests.get(config.API_PRECO_ATUAL, params=parametros, timeout=15)
        resposta.raise_for_status()
        dados = resposta.json()
        return float(dados["bitcoin"][moeda])
    except (requests.RequestException, KeyError, ValueError) as exc:
        raise ErroAPI(f"Falha ao obter preço atual: {exc}") from exc


def obter_historico_precos(
    dias: int = config.DIAS_HISTORICO,
    moeda: str = config.MOEDA_FIAT,
) -> list[float]:
    parametros = {"vs_currency": moeda, "days": dias, "interval": "daily"}
    try:
        resposta = requests.get(config.API_HISTORICO, params=parametros, timeout=20)
        resposta.raise_for_status()
        dados = resposta.json()
        return [float(ponto[1]) for ponto in dados["prices"]]
    except (requests.RequestException, KeyError, ValueError) as exc:
        raise ErroAPI(f"Falha ao obter histórico: {exc}") from exc
