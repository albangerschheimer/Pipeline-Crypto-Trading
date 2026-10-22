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
│   └── universe.py    # Univers des 50 cryptos (hors stablecoins et or tokenisé)
├── main.py            # Point d'entrée : télécharge les bougies 1h des 50 cryptos dans crypto.db
├── explore.ipynb      # Exploration des API Binance et CoinGecko
├── .env.example       # Modèle des variables d'environnement (sans valeurs)
└── requirements.txt   # Dépendances Python
```

Lancer : `.venv/bin/python main.py`

## Avancement

- [x] Exploration des API (notebook)
- [x] **Étape 0** : projet reproductible (README, dépendances, secrets)
- [x] **Étape 1** : passer du notebook à des modules Python
- [x] **Étape 2** : extraction robuste (pagination, rate limits, retries, logging)
- [x] **Étape 3** : stockage en base de données
- [x] **Étape 4** : ingestion incrémentale et idempotente
- [ ] **Étape 5** : contrôles qualité (cohérence des prix, trous)
- [ ] **Étape 6** : stratégie et backtest (avec ses indicateurs)
- [ ] **Étape 7** : automatisation (cron)
- [ ] *Optionnel* : tableau de bord
