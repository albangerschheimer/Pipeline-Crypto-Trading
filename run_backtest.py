from pipeline.backtest import backtest, crossover_positions, load_closes
from pipeline.db import connect

INTERVAL = "1h"
FAST, SLOW = 20, 50

conn = connect()
symbols = [row[0] for row in conn.execute(
    "SELECT DISTINCT symbol FROM klines WHERE interval = ? ORDER BY symbol", (INTERVAL,)
)]

results = []
print(f"{'symbole':<12}{'stratégie':>11}{'buy & hold':>12}{'trades':>8}{'drawdown max':>14}")
for symbol in symbols:
    closes = load_closes(conn, symbol, INTERVAL)
    if len(closes) <= SLOW:
        continue
    r = backtest(closes, crossover_positions(closes, FAST, SLOW))
    results.append(r)
    print(f"{symbol:<12}{r['return']:>11.1%}{r['buy_hold']:>12.1%}{r['trades']:>8}{r['max_drawdown']:>14.1%}")

n = len(results)
beats = sum(r["return"] > r["buy_hold"] for r in results)
print(f"\nMoyenne sur {n} cryptos : stratégie {sum(r['return'] for r in results) / n:.1%}, "
      f"buy & hold {sum(r['buy_hold'] for r in results) / n:.1%}")
print(f"La stratégie bat le buy & hold sur {beats}/{n} cryptos")
