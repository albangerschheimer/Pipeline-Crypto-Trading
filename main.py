from pipeline.binance import get_klines, get_usdt_symbols

bougies = get_klines("BTCUSDT", limit=2)
print(bougies)

symboles = get_usdt_symbols()
print(len(symboles), "paires USDT")
