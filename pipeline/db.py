import sqlite3
from datetime import datetime

DB_PATH = "crypto.db"


def connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute("""CREATE TABLE IF NOT EXISTS klines (
        symbol TEXT,
        interval TEXT,
        open_time TEXT,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume REAL,
        close_time TEXT,
        quote_asset_volume REAL,
        number_of_trades INTEGER,
        taker_buy_base_asset_volume REAL,
        taker_buy_quote_asset_volume REAL,
        PRIMARY KEY (symbol, interval, open_time)
    )""")


def save_klines(conn: sqlite3.Connection, symbol: str, interval: str, klines: list[dict]) -> None:
    rows = [
        (
            symbol, interval, k["open_time"].isoformat(),
            k["open"], k["high"], k["low"], k["close"], k["volume"],
            k["close_time"].isoformat(), k["quote_asset_volume"], k["number_of_trades"],
            k["taker_buy_base_asset_volume"], k["taker_buy_quote_asset_volume"],
        )
        for k in klines
    ]
    with conn:
        conn.executemany("""INSERT OR REPLACE INTO klines (
            symbol, interval, open_time, open, high, low, close, volume,
            close_time, quote_asset_volume, number_of_trades,
            taker_buy_base_asset_volume, taker_buy_quote_asset_volume
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", rows)

def get_last_open_time(conn: sqlite3.Connection, symbol: str, interval: str) -> datetime | None:
    row = conn.execute(
        "SELECT max(open_time) FROM klines WHERE symbol = ? AND interval = ?",
        (symbol, interval),
    ).fetchone()
    return datetime.fromisoformat(row[0]) if row[0] else None   