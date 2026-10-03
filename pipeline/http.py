import logging
import time

import httpx

log = logging.getLogger(__name__)

RETRY_STATUSES = {429, 500, 502, 503, 504}


def get_json(url: str, params: dict | None = None, headers: dict | None = None, retries: int = 4):
    for attempt in range(retries + 1):
        try:
            response = httpx.get(url, params=params, headers=headers, timeout=10)
            if response.status_code not in RETRY_STATUSES:
                response.raise_for_status()  
                return response.json()
            reason = f"HTTP {response.status_code}"
        except httpx.TransportError as e:
            reason = f"erreur réseau ({e})"

        if attempt == retries:
            raise RuntimeError(f"Impossible de récupérer {url} : {reason}")

        wait = 2 ** attempt
        log.warning("%s sur %s, nouvelle tentative dans %ss", reason, url, wait)
        time.sleep(wait)