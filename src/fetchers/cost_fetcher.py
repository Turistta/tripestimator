import logging

import requests
from requests.exceptions import HTTPError

from fetchers.base_fetcher import BaseFetcher

logger = logging.getLogger(__name__)


class CostFetcher(BaseFetcher):
    def fetch(self, state: str) -> str:
        endpoint = self.BASE_URL + state
        self.source_url = endpoint
        logger.info(f"Fetching raw data from URL: {endpoint}")
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            logger.info("Successfully fetched raw data.")
            return response.text
        except HTTPError as e:
            logger.error(f"Request error for URL {endpoint}: {e}")
            raise

    @property
    def BASE_URL(self):
        return "https://precos.petrobras.com.br/web/precos-dos-combustiveis/w/gasolina/"
