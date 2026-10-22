import time

from pipeline.http import get_json
from pipeline.config import COINGECKO_API_KEY

BASE_URL = "https://api.coingecko.com/api/v3"
HEADERS = {"x-cg-demo-api-key": COINGECKO_API_KEY}
MIN_INTERVAL = 60 / 30  


def _get(path: str, params: dict | None = None):
    time.sleep(MIN_INTERVAL)
    return get_json(f"{BASE_URL}{path}", params=params, headers=HEADERS)


def get_top_markets(n: int = 150, category: str | None = None) -> list[dict]:
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": n, "page": 1}
    if category:
        params["category"] = category
    return _get("/coins/markets", params=params)


def get_coin_social(coin_id: str) -> dict:
    params = {"localization": "false", "tickers": "false", "market_data": "false"}
    details = _get(f"/coins/{coin_id}", params=params)
    return {
        "sentiment_votes_up_pct": details["sentiment_votes_up_percentage"],
        "sentiment_votes_down_pct": details["sentiment_votes_down_percentage"],
        "watchlist_portfolio_users": details["watchlist_portfolio_users"],
        "market_cap_rank": details["market_cap_rank"],
    }
