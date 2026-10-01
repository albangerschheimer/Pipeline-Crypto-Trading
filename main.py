from pipeline.binance import get_klines, get_usdt_symbols
from pipeline.coingecko import get_top_markets, get_coin_social

bougies = get_klines("BTCUSDT", limit=2)
print(bougies)

symboles = get_usdt_symbols()
print(len(symboles), "paires USDT")

top = get_top_markets(5)
for coin in top:
    print(coin["market_cap_rank"], coin["id"], coin["current_price"])

print(get_coin_social("bitcoin"))
