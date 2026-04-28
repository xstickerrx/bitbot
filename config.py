"""Configurações do BitBot."""

MOEDA_FIAT = "brl"

INTERVALO_VERIFICACAO_SEGUNDOS = 60

DIAS_HISTORICO = 90

PERIODO_SMA_CURTA = 7
PERIODO_SMA_LONGA = 30
PERIODO_RSI = 14

RSI_SOBREVENDIDO = 30
RSI_SOBRECOMPRADO = 70

DESVIO_FORTE = 0.05

ARQUIVO_LOG = "bitbot.log"

API_PRECO_ATUAL = "https://api.coingecko.com/api/v3/simple/price"
API_HISTORICO = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
