import logging

import requests
from requests.exceptions import HTTPError
from requests.models import PreparedRequest

from fetchers.base_fetcher import BaseFetcher
from models.utils_models import BaseQueryParams

logger = logging.getLogger(__name__)


class PlaceFetcher(BaseFetcher):
    def fetch(self, params: BaseQueryParams) -> str:
        params_dict = params.model_dump()
        query_type = params_dict.pop("query_type")
        endpoint = self.BASE_URL.format(query_type=query_type)
        self.source_url = endpoint
        req = PreparedRequest()
        params_dict["key"] = params_dict.pop("api_key")
        params_dict["input"] = params_dict.pop("text_input")
        req.prepare_url(endpoint, params_dict)
        try:
            response = requests.get(url=req.url)  # type: ignore
            response.raise_for_status()
            logger.info("Successfully fetched raw data.")
            self.source_url = req.url  # type: ignore
            return response.text
        except HTTPError as e:
            logger.error(f"Request error for URL {req.url}: {e}")
            raise

    # TODO: Fix 'reviews' keyword.

    @property
    def BASE_URL(self):
        return (
            "https://maps.googleapis.com/maps/api/place/{query_type}/json?fields=formatted_address,name,geometry"
            + ",opening_hours,business_status,place_id,plus_code,type,rating,photos,price_level,user_ratings_total"
        )
