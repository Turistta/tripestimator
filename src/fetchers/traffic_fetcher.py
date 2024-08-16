import asyncio
import json
import logging
from typing import Optional

import aiohttp

from fetchers.base_fetcher import BaseFetcher
from models.traffic_models import TrafficQueryParams
from models.utils_models import Coordinates

logger = logging.getLogger(__name__)


class TrafficFetcher(BaseFetcher):

    async def fetch(self, params: TrafficQueryParams) -> str:
        coordinates = params.get_coordinates()
        bbox = f"{','.join(map(str, params.get_bounding_boxes_coords(coordinates)))}"
        query_params = {
            "key": params.api_key,
            "bbox": bbox,
            "fields": "{incidents{type,geometry{type,coordinates},properties{iconCategory}}}",
            "language": "pt-PT",
            "t": "1111",
            "timeValidityFilter": "present",
        }

        async with aiohttp.ClientSession() as session:
            incidents_data = await self._fetch_data(session, self.EXTRA_URL, params=query_params)
            traffic_data = await self._fetch_traffic_data(
                session, self.BASE_URL.format(api_key=params.api_key), coordinates
            )

        return json.dumps({"incidents_data": incidents_data, "traffic_data": traffic_data})

    async def _fetch_data(self, session: aiohttp.ClientSession, url: str, params: Optional[dict] = None) -> str:
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    logger.info(f"Successfully fetched data from {url}")
                    return await response.text()
                logger.error(f"{__name__} raised for status: {response.status}")
                raise aiohttp.ClientResponseError(response.request_info, response.history, status=response.status)
        except aiohttp.ClientError as e:
            logger.error(f"Request error for URL {url}: {e}")
            raise

    async def _fetch_traffic_data(
        self, session: aiohttp.ClientSession, url: str, coordinates: list[Coordinates]
    ) -> list:
        async def fetch_traffic(coordinates: Coordinates):
            endpoint = f"{url}{coordinates.latitude},{coordinates.longitude}"
            return await self._fetch_data(session=session, url=endpoint)

        tasks = [fetch_traffic(c) for c in coordinates]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        return [str(result) if isinstance(result, Exception) else result for result in results]

    @property
    def BASE_URL(self):
        return "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={api_key}&point="

    @property
    def EXTRA_URL(self):
        return "https://api.tomtom.com/traffic/services/5/incidentDetails"
