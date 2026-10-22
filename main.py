import logging
import sys
from datetime import datetime, timedelta, timezone

from pipeline.binance import get_klines_range
from pipeline.db import connect, get_last_open_time, init_db, save_klines
from pipeline.quality import count_gaps, count_invalid_klines
from pipeline.universe import build_universe

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger(__name__)

conn = connect()
init_db(conn)

INTERVAL = "1h"
end = datetime.now(timezone.utc)

failures = []

for crypto in build_universe():
    symbol = crypto["binance_symbol"]
    try:
        start = get_last_open_time(conn, symbol, INTERVAL) or end - timedelta(days=30)
        klines = get_klines_range(symbol, start, end, interval=INTERVAL)
        save_klines(conn, symbol, INTERVAL, klines)
        log.info("%s : %d bougies depuis %s", symbol, len(klines), start)
    except Exception:
        log.exception("Erreur lors de la récupération des bougies pour %s", symbol)
        failures.append(symbol)

log.info("Récupération des bougies terminée avec %d échec(s) : %s", len(failures), ", ".join(failures))

invalid = count_invalid_klines(conn)
gaps = count_gaps(conn, INTERVAL, 3600)
log.info("Qualité : %d bougies incohérentes, %d trous", invalid, gaps)

sys.exit(1 if failures or invalid or gaps else 0)

