import logging
from typing import Final

import requests
from requests.exceptions import HTTPError

BASE_URL: Final = "https://precos.petrobras.com.br/web/precos-dos-combustiveis/w/gasolina/"

logger = logging.getLogger(__name__)


class CostFetcher:
    def fetch(self, state: str) -> str:
        endpoint = BASE_URL + state
        logger.info(f"Fetching raw data from URL: {endpoint}")
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            logger.info("Successfully fetched raw data.")
            return response.text
        except HTTPError as e:
            logger.error(f"Request error for URL {endpoint}: {e}")
            raise
