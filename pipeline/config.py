import os
from dotenv import load_dotenv

load_dotenv()

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
if not COINGECKO_API_KEY:
    raise RuntimeError(
        "COINGECKO_API_KEY manquante : copie .env.example en .env et remplis-la"
    )
