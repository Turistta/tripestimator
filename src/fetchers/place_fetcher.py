import logging
import urllib
import urllib.parse

import aiohttp

from fetchers.base_fetcher import BaseFetcher
from models.utils_models import BaseQueryParams

logger = logging.getLogger(__name__)


class PlaceFetcher(BaseFetcher):
    async def fetch(self, params: BaseQueryParams) -> str:
        params_dict = params.model_dump(exclude_none=True)
        query_type = params_dict.pop("query_type")
        endpoint = self.BASE_URL.format(query_type=query_type)
        params_dict["key"] = params_dict.pop("api_key")
        params_dict["input"] = params_dict.pop("text_input")
        # TODO: #6 fix other type of place queries
        encoded_params = urllib.parse.urlencode(params_dict)
        url = f"{endpoint}&{encoded_params}"
        self.source_url = url
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url=url) as response:
                    if response.status == 200:
                        logger.info("Successfully fetched raw data.")
                        return await response.text()
                    logger.error(f"{__name__} raised for status: {response.status}")
                    raise
            except aiohttp.ClientConnectionError as e:
                logger.error(f"Request error for URL {endpoint}: {e}")
                raise e

    @property
    def BASE_URL(self):
        return (
            "https://maps.googleapis.com/maps/api/place/{query_type}/json?fields=formatted_address,name,geometry"
            + ",opening_hours,business_status,place_id,plus_code,type,rating,photos,price_level,user_ratings_total"
        )
        # TODO: #7 Fix 'reviews' keyword.
