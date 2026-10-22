# Pipeline Crypto Trading

Pipeline de données qui collecte les prix (Binance) et les données de marché (CoinGecko) d'un univers de 50 cryptomonnaies, pour les stocker, les transformer et tester des stratégies de trading.

> Projet d'apprentissage, construit étape par étape.

## Sources de données

| Source | Utilisation | Clé API |
|---|---|---|
| [Binance](https://developers.binance.com/docs/binance-spot-api-docs/rest-api) | Bougies OHLCV (`/api/v3/klines`), liste des paires (`/api/v3/exchangeInfo`) | Non |
| [CoinGecko](https://docs.coingecko.com/v3.0.1/reference/introduction) | Classement par capitalisation (`/coins/markets`), données sociales (`/coins/{id}`) | Oui (plan Demo gratuit) |

## Installation

Prérequis : Python 3.13

```bash
# 1. Cloner le dépôt
git clone https://github.com/albangerschheimer/Pipeline-Crypto-Trading.git
cd Pipeline-Crypto-Trading

# 2. Créer et activer l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les secrets
cp .env.example .env
# puis remplir COINGECKO_API_KEY dans .env
```

Une clé CoinGecko gratuite s'obtient sur [coingecko.com/en/api](https://www.coingecko.com/en/api).

## Structure

```
.
├── pipeline/
│   ├── config.py      # Lecture du .env (clé API)
│   ├── binance.py     # Client Binance : bougies (paginées), paires USDT
│   ├── coingecko.py   # Client CoinGecko : classement, données sociales (30 appels/min)
│   ├── db.py          # Base SQLite : table klines, écriture, dernière bougie connue
│   ├── http.py        # get_json : nouvelles tentatives et logging
│   ├── quality.py     # Contrôles qualité : prix incohérents, trous
│   ├── backtest.py    # Moyennes mobiles et simulation de la stratégie
│   └── universe.py    # Univers des 50 cryptos (hors stablecoins et or tokenisé)
├── main.py            # Pipeline : télécharge les bougies 1h des 50 cryptos dans crypto.db
├── run_backtest.py    # Backtest de la stratégie sur toute la base
├── test_backtest.py   # Vérifications du backtest
├── explore.ipynb      # Exploration des API Binance et CoinGecko
├── .env.example       # Modèle des variables d'environnement (sans valeurs)
└── requirements.txt   # Dépendances Python
```

## Utilisation

```bash
.venv/bin/python main.py           # récupère les nouvelles bougies (180 jours au premier lancement)
.venv/bin/python run_backtest.py   # teste la stratégie sur les données en base
.venv/bin/python test_backtest.py  # vérifie les calculs du backtest
```

`main.py` se termine avec le code `1` si une crypto a échoué ou si un contrôle qualité a trouvé un problème.

## Stratégie

Croisement de moyennes mobiles sur les bougies 1h : investi quand la moyenne des 20 dernières clôtures passe au-dessus de celle des 50 dernières, hors marché sinon. Frais de 0,1 % par ordre. La position est décidée à la clôture d'une bougie et appliquée à la suivante (pas de triche sur les prix futurs).

Résultat sur 180 jours (octobre 2026) : +12,1 % en moyenne contre +31,1 % pour le buy & hold, la stratégie ne bat le buy & hold que sur 20 cryptos sur 50. Une stratégie aussi simple ne suffit pas : c'est le point de départ pour en tester d'autres.

## Automatisation

Lancer le pipeline toutes les heures avec cron (`crontab -e`) :

```
5 * * * * cd /Users/alban/GitHub/Pipeline-Crypto-Trading && .venv/bin/python main.py >> pipeline.log 2>&1
```

À la 5ᵉ minute de chaque heure, pour que la bougie précédente soit clôturée. Si le Mac est en veille, le lancement est manqué, mais le suivant rattrape tout seul les bougies manquantes grâce à l'ingestion incrémentale.

## Avancement

- [x] Exploration des API (notebook)
- [x] **Étape 0** : projet reproductible (README, dépendances, secrets)
- [x] **Étape 1** : passer du notebook à des modules Python
- [x] **Étape 2** : extraction robuste (pagination, rate limits, retries, logging)
- [x] **Étape 3** : stockage en base de données
- [x] **Étape 4** : ingestion incrémentale et idempotente
- [x] **Étape 5** : contrôles qualité (cohérence des prix, trous)
- [x] **Étape 6** : stratégie et backtest (avec ses indicateurs)
- [x] **Étape 7** : automatisation (cron)
- [ ] *Optionnel* : tableau de bord
