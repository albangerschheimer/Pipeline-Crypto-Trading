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
├── explore.ipynb      # Exploration des API Binance et CoinGecko
├── .env.example       # Modèle des variables d'environnement (sans valeurs)
└── requirements.txt   # Dépendances Python
```

## Avancement

- [x] Exploration des API (notebook)
- [ ] **Étape 0** : projet reproductible (README, dépendances, secrets)
- [ ] **Étape 1** : passer du notebook à des modules Python
- [ ] **Étape 2** : extraction robuste (pagination, rate limits, retries, logging)
- [ ] **Étape 3** : stockage en base de données
- [ ] **Étape 4** : ingestion incrémentale et idempotente
- [ ] **Étape 5** : qualité des données et tests
- [ ] **Étape 6** : transformations et indicateurs
- [ ] **Étape 7** : stratégie et backtest
- [ ] **Étape 8** : automatisation
- [ ] **Étape 9** : tableau de bord
