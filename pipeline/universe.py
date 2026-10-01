from pipeline.binance import get_usdt_symbols
from pipeline.coingecko import get_top_markets

EXCLUDED_CATEGORIES = ["stablecoins", "tokenized-commodities"]


def get_excluded_ids() -> set[str]:
    excluded = set()
    for category in EXCLUDED_CATEGORIES:
        excluded |= {coin["id"] for coin in get_top_markets(250, category=category)}
    return excluded


def build_universe(size: int = 50) -> list[dict]:
    usdt_symbols = get_usdt_symbols()
    excluded = get_excluded_ids()

    universe = []
    seen = set()
    for coin in get_top_markets(250):
        binance_symbol = coin["symbol"].upper() + "USDT"
        if coin["id"] in excluded or binance_symbol not in usdt_symbols or binance_symbol in seen:
            continue
        seen.add(binance_symbol)
        universe.append({
            "coingecko_id": coin["id"],
            "symbol": coin["symbol"],
            "binance_symbol": binance_symbol,
            "market_cap_rank": coin["market_cap_rank"],
        })
        if len(universe) == size:
            return universe

    raise RuntimeError(f"Univers incomplet : {len(universe)}/{size} cryptos trouvées")
