import logging

import aiohttp

from fetchers.base_fetcher import BaseFetcher

logger = logging.getLogger(__name__)


class CostFetcher(BaseFetcher):
    async def fetch(self, state: str) -> str:
        endpoint = self.BASE_URL + state
        self.source_url = endpoint
        logger.info(f"Fetching raw data from URL: {endpoint}")
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(endpoint) as response:
                    if response.status == 200:
                        logger.info("Successfully fetched raw data.")
                        return await response.text()
                    logger.error(f"{__name__} raised for status: {response.status}")
                    raise
            except aiohttp.ClientConnectionError as e:
                logger.error(f"Request error for URL {endpoint}: {e}")
                raise

    @property
    def BASE_URL(self):
        return "https://precos.petrobras.com.br/web/precos-dos-combustiveis/w/gasolina/"
