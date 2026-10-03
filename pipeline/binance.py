from pipeline.http import get_json
from datetime import datetime, timezone

BASE_URL = "https://api.binance.com/api/v3"


def parse_klines(raw_klines: list) -> list[dict]:
    klines = []
    for raw in raw_klines:
        klines.append({
            "open_time": datetime.fromtimestamp(raw[0] / 1000, tz=timezone.utc),
            "open": float(raw[1]),
            "high": float(raw[2]),
            "low": float(raw[3]),
            "close": float(raw[4]),
            "volume": float(raw[5]),
            "close_time": datetime.fromtimestamp(raw[6] / 1000, tz=timezone.utc),
            "quote_asset_volume": float(raw[7]),
            "number_of_trades": int(raw[8]),
            "taker_buy_base_asset_volume": float(raw[9]),
            "taker_buy_quote_asset_volume": float(raw[10]),
        })
    return klines


def get_klines(symbol: str, interval: str = "1m", limit: int = 500) -> list[dict]:
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    return parse_klines(get_json(f"{BASE_URL}/klines", params=params))


def get_usdt_symbols() -> set[str]:
    data = get_json(f"{BASE_URL}/exchangeInfo")
    return {
        s["symbol"]
        for s in data["symbols"]
        if s["quoteAsset"] == "USDT" and s["status"] == "TRADING"
    }
