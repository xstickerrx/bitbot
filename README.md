# BitBot

Monitor de cotação do **Bitcoin** em tempo real, escrito em Python. O BitBot consulta o preço atual e o histórico recente do BTC, calcula indicadores técnicos (médias móveis e RSI) e imprime no terminal sinais de **COMPRA**, **VENDA** ou **AGUARDAR** com sua respectiva força (`FORTE`, `MODERADO`, `NEUTRO`).

Tudo é registrado em arquivo de log para análise posterior.

---

## Funcionalidades

- Cotação atual do Bitcoin via API pública da [CoinGecko](https://www.coingecko.com/) (sem chave de API).
- Histórico de até 90 dias atualizado automaticamente a cada hora.
- Indicadores técnicos calculados em Python puro:
  - **SMA 7** — Média Móvel Simples curta
  - **SMA 30** — Média Móvel Simples longa
  - **RSI 14** — Índice de Força Relativa
- Recomendações automáticas baseadas em pontuação combinada dos indicadores.
- Saída colorida no terminal (verde/compra, vermelho/venda, amarelo/aguardar).
- Log estruturado em `bitbot.log`.
- Totalmente configurável via `config.py` (moeda, intervalos, limites de RSI etc.).

---

## Estrutura do Projeto

```
bitbot/
├── bitbot.py          # Loop principal e interface no terminal
├── api.py             # Cliente HTTP da CoinGecko
├── analise.py         # Lógica de decisão (gera os sinais)
├── indicadores.py     # SMA, RSI e desvio percentual
├── config.py          # Parâmetros configuráveis
├── requirements.txt   # Dependências
└── README.md
```

---

## Requisitos

- Python **3.10+**
- Acesso à internet (para consultar a API da CoinGecko)

Dependências instaladas via `pip`:

- `requests` — chamadas HTTP
- `colorama` — cores no terminal

---

## Instalação

Clone ou baixe o projeto e, dentro da pasta `bitbot/`, execute:

```bash
# Cria um ambiente virtual isolado
python3 -m venv .venv

# Ativa o ambiente
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows

# Instala as dependências
pip install -r requirements.txt
```

---

## Como executar

Com o ambiente virtual ativado:

```bash
python bitbot.py
```

Ou diretamente, sem ativar:

```bash
.venv/bin/python bitbot.py
```

Para encerrar, pressione **Ctrl+C**.

---

## Exemplo de saída

```
    ____  _ _   ____        _
   | __ )(_) |_| __ )  ___ | |_
   |  _ \| | __|  _ \ / _ \| __|
   | |_) | | |_| |_) | (_) | |_
   |____/|_|\__|____/ \___/ \__|

  Monitor de Bitcoin em BRL — intervalo: 60s
  Indicadores: SMA7, SMA30, RSI(14)
  Pressione Ctrl+C para encerrar.

──────────────────────────────────────────────────────────────────────────────
[28/04/2026 13:58:43] VENDER (MODERADO)
  Preço atual ........ R$ 380.179,00
  SMA7   ............... R$ 386.895,25
  SMA30  ............... R$ 370.522,04  (desvio: +2.61%)
  RSI(14) ............. 54.6
  Motivo ............. preço 2.61% acima da SMA30; SMA7 acima da SMA30 (tendência de alta recente); RSI=54.6 em zona neutra
```

---

## Como o sinal é gerado

A cada ciclo, o BitBot pontua a situação atual do mercado a partir de três indicadores. Cada condição soma pontos do lado da **compra** ou da **venda**:

| Condição                                    | Compra | Venda |
|---------------------------------------------|:------:|:-----:|
| Preço abaixo da SMA30                       | +1     |       |
| Preço acima da SMA30                        |        | +1    |
| SMA7 abaixo da SMA30 (tendência de baixa)   | +1     |       |
| SMA7 acima da SMA30 (tendência de alta)     |        | +1    |
| RSI ≤ 30 (sobrevenda)                       | +2     |       |
| RSI ≥ 70 (sobrecompra)                      |        | +2    |
| Desvio ≥ 5% abaixo/acima da SMA30           | +1     | +1    |

O lado com mais pontos define a ação:

- **2 pontos** → recomendação **MODERADA**
- **3 pontos ou mais** → recomendação **FORTE**
- Empate ou pontuação insuficiente → **AGUARDAR**

---

## Configuração

Abra `config.py` para ajustar o comportamento do bot:

```python
MOEDA_FIAT = "brl"                       # ou "usd"
INTERVALO_VERIFICACAO_SEGUNDOS = 60      # frequência das checagens
DIAS_HISTORICO = 90                      # janela usada nos indicadores

PERIODO_SMA_CURTA = 7
PERIODO_SMA_LONGA = 30
PERIODO_RSI = 14

RSI_SOBREVENDIDO = 30                    # limite p/ sinal forte de compra
RSI_SOBRECOMPRADO = 70                   # limite p/ sinal forte de venda
DESVIO_FORTE = 0.05                      # 5% de afastamento da SMA30

ARQUIVO_LOG = "bitbot.log"
```

---

## Logs

Cada decisão é registrada em `bitbot.log` no formato:

```
2026-04-28 13:58:43 | INFO | VENDER|MODERADO|preco=380179.00|sma_curta=386895.25|sma_longa=370522.04|rsi=54.60|desvio=0.0261|motivo=...
```

Útil para auditoria, gráficos posteriores ou backtests manuais.

---

## Aviso Legal

O BitBot é uma ferramenta **educacional** que aplica indicadores técnicos clássicos. Ele **não é uma recomendação de investimento**. Criptomoedas são ativos voláteis e qualquer decisão de compra ou venda é de responsabilidade do usuário. Use por sua conta e risco.

---

## Licença

Uso pessoal e livre. Sinta-se à vontade para adaptar.
