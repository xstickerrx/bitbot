"""BitBot — monitor de cotação do Bitcoin com sinais de compra e venda."""

from __future__ import annotations

import logging
import time
from datetime import datetime

from colorama import Fore, Style, init as colorama_init

import config
from analise import Sinal, analisar
from api import ErroAPI, obter_historico_precos, obter_preco_atual

colorama_init(autoreset=True)

logging.basicConfig(
    filename=config.ARQUIVO_LOG,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def formatar_moeda(valor: float, moeda: str = config.MOEDA_FIAT) -> str:
    if moeda.lower() == "brl":
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if moeda.lower() == "usd":
        return f"US$ {valor:,.2f}"
    return f"{valor:,.2f} {moeda.upper()}"


def cor_para_acao(acao: str) -> str:
    if acao == "COMPRAR":
        return Fore.GREEN + Style.BRIGHT
    if acao == "VENDER":
        return Fore.RED + Style.BRIGHT
    return Fore.YELLOW + Style.BRIGHT


def imprimir_sinal(sinal: Sinal) -> None:
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    cor = cor_para_acao(sinal.acao)
    cabecalho = f"[{agora}] {cor}{sinal.acao} ({sinal.forca}){Style.RESET_ALL}"
    preco = formatar_moeda(sinal.preco_atual)
    sma_curta = formatar_moeda(sinal.sma_curta) if sinal.sma_curta else "—"
    sma_longa = formatar_moeda(sinal.sma_longa) if sinal.sma_longa else "—"
    rsi_txt = f"{sinal.rsi:.1f}" if sinal.rsi is not None else "—"
    desvio_txt = f"{sinal.desvio_sma_longa * 100:+.2f}%"

    print("─" * 78)
    print(cabecalho)
    print(f"  Preço atual ........ {Fore.CYAN}{preco}{Style.RESET_ALL}")
    print(f"  SMA{config.PERIODO_SMA_CURTA:<3} ............... {sma_curta}")
    print(f"  SMA{config.PERIODO_SMA_LONGA:<3} ............... {sma_longa}  (desvio: {desvio_txt})")
    print(f"  RSI({config.PERIODO_RSI}) ............. {rsi_txt}")
    print(f"  Motivo ............. {sinal.motivo}")


def registrar_log(sinal: Sinal) -> None:
    logging.info(
        "%s|%s|preco=%.2f|sma_curta=%s|sma_longa=%s|rsi=%s|desvio=%.4f|motivo=%s",
        sinal.acao,
        sinal.forca,
        sinal.preco_atual,
        f"{sinal.sma_curta:.2f}" if sinal.sma_curta else "NA",
        f"{sinal.sma_longa:.2f}" if sinal.sma_longa else "NA",
        f"{sinal.rsi:.2f}" if sinal.rsi is not None else "NA",
        sinal.desvio_sma_longa,
        sinal.motivo,
    )


def banner() -> None:
    print(Fore.MAGENTA + Style.BRIGHT + r"""
    ____  _ _   ____        _
   | __ )(_) |_| __ )  ___ | |_
   |  _ \| | __|  _ \ / _ \| __|
   | |_) | | |_| |_) | (_) | |_
   |____/|_|\__|____/ \___/ \__|
""" + Style.RESET_ALL)
    print(f"  Monitor de Bitcoin em {config.MOEDA_FIAT.upper()} — intervalo: {config.INTERVALO_VERIFICACAO_SEGUNDOS}s")
    print(f"  Indicadores: SMA{config.PERIODO_SMA_CURTA}, SMA{config.PERIODO_SMA_LONGA}, RSI({config.PERIODO_RSI})")
    print(f"  Pressione Ctrl+C para encerrar.\n")


def executar() -> None:
    banner()
    historico_cache: list[float] = []
    ultima_atualizacao_historico = 0.0
    INTERVALO_HISTORICO = 60 * 60  # 1h

    while True:
        try:
            agora = time.time()
            if not historico_cache or (agora - ultima_atualizacao_historico) > INTERVALO_HISTORICO:
                historico_cache = obter_historico_precos()
                ultima_atualizacao_historico = agora

            preco_atual = obter_preco_atual()
            sinal = analisar(preco_atual, historico_cache)
            imprimir_sinal(sinal)
            registrar_log(sinal)

        except ErroAPI as exc:
            print(Fore.RED + f"[erro de API] {exc}" + Style.RESET_ALL)
            logging.error("Erro de API: %s", exc)
        except Exception as exc:  # noqa: BLE001
            print(Fore.RED + f"[erro inesperado] {exc}" + Style.RESET_ALL)
            logging.exception("Erro inesperado")

        try:
            time.sleep(config.INTERVALO_VERIFICACAO_SEGUNDOS)
        except KeyboardInterrupt:
            break


def main() -> None:
    try:
        executar()
    except KeyboardInterrupt:
        print(Fore.MAGENTA + "\nEncerrando BitBot. Até a próxima!" + Style.RESET_ALL)


if __name__ == "__main__":
    main()
