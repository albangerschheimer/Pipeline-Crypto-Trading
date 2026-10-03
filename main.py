import logging

from pipeline.universe import build_universe

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

univers = build_universe()
print(len(univers), "cryptos")
for crypto in univers:
    print(crypto["market_cap_rank"], crypto["binance_symbol"])
