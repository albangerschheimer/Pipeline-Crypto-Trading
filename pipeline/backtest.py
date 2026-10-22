import sqlite3

FEE = 0.001  # frais Binance spot : 0,1 % par ordre


def load_closes(conn: sqlite3.Connection, symbol: str, interval: str) -> list[float]:
    rows = conn.execute(
        "SELECT close FROM klines WHERE symbol = ? AND interval = ? ORDER BY open_time",
        (symbol, interval),
    )
    return [row[0] for row in rows]


def sma(values: list[float], n: int) -> list[float | None]:
    """Moyenne mobile simple sur n valeurs, None tant qu'il n'y en a pas assez."""
    result = [None] * len(values)
    total = 0.0
    for i, value in enumerate(values):
        total += value
        if i >= n:
            total -= values[i - n]
        if i >= n - 1:
            result[i] = total / n
    return result


def crossover_positions(closes: list[float], fast: int = 20, slow: int = 50) -> list[int]:
    """1 (investi) quand la moyenne rapide est au-dessus de la lente, sinon 0."""
    fast_sma, slow_sma = sma(closes, fast), sma(closes, slow)
    return [int(f is not None and s is not None and f > s) for f, s in zip(fast_sma, slow_sma)]


def backtest(closes: list[float], positions: list[int], fee: float = FEE) -> dict:
    equity, peak, max_drawdown, trades = 1.0, 1.0, 0.0, 0
    held = 0
    for i in range(1, len(closes)):
        # La position décidée à la clôture i-1 s'applique au rendement de la bougie i :
        # on ne trade jamais sur un prix qu'on ne connaissait pas encore.
        if positions[i - 1] != held:
            held = positions[i - 1]
            equity *= 1 - fee
            trades += 1
        equity *= 1 + held * (closes[i] / closes[i - 1] - 1)
        peak = max(peak, equity)
        max_drawdown = max(max_drawdown, 1 - equity / peak)
    return {
        "return": equity - 1,
        "buy_hold": closes[-1] / closes[0] - 1,
        "trades": trades,
        "max_drawdown": max_drawdown,
    }
