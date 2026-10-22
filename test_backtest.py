from pipeline.backtest import backtest, crossover_positions, sma

# Moyenne mobile : None tant qu'il n'y a pas assez de valeurs
assert sma([1, 2, 3, 4], 2) == [None, 1.5, 2.5, 3.5]

# Toujours investi sur un prix qui double : +100 %, moins les frais d'un seul achat
r = backtest([100, 150, 200], [1, 1, 1], fee=0.001)
assert abs(r["return"] - (2 * 0.999 - 1)) < 1e-9
assert r["trades"] == 1 and r["buy_hold"] == 1.0

# Jamais investi : rien ne bouge, aucun trade
assert backtest([100, 50, 200], [0, 0, 0])["return"] == 0

# Pas de triche : la position prise à la clôture d'une bougie ne profite pas de cette bougie
assert backtest([100, 200], [0, 1])["return"] == 0

# Drawdown : de 200 à 100, on perd 50 % depuis le sommet
assert abs(backtest([100, 200, 100], [1, 1, 1], fee=0)["max_drawdown"] - 0.5) < 1e-9

# Tendance haussière : la moyenne rapide passe au-dessus de la lente
assert crossover_positions(list(range(1, 100)), fast=5, slow=10)[-1] == 1

print("OK")
