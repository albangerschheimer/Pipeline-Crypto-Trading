from pipeline.universe import build_universe

univers = build_universe()
print(len(univers), "cryptos")
for crypto in univers:
    print(crypto["market_cap_rank"], crypto["binance_symbol"])
