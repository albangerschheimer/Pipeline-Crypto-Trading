from pipeline.backtest import backtest, crossover_positions, sma

assert sma([1, 2, 3, 4], 2) == [None, 1.5, 2.5, 3.5]

r = backtest([100, 150, 200], [1, 1, 1], fee=0.001)
assert abs(r["return"] - (2 * 0.999 - 1)) < 1e-9
assert r["trades"] == 1 and r["buy_hold"] == 1.0

assert backtest([100, 50, 200], [0, 0, 0])["return"] == 0

assert backtest([100, 200], [0, 1])["return"] == 0

assert abs(backtest([100, 200, 100], [1, 1, 1], fee=0)["max_drawdown"] - 0.5) < 1e-9

assert crossover_positions(list(range(1, 100)), fast=5, slow=10)[-1] == 1

print("OK")
