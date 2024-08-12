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
        query_type = params_dict.pop("_query_type")
        endpoint = self.BASE_URL.format(query_type=query_type)
        self.source_url = endpoint
        req = PreparedRequest()
        params_dict["key"] = params.api_key
        req.prepare_url(endpoint, params_dict)

        try:
            response = requests.get(url=req.url)  # type: ignore
            response.raise_for_status()
            logger.info("Successfully fetched raw data.")
            self.source_url = req.url  # Set the source_url # type: ignore
            return response.text
        except HTTPError as e:
            logger.error(f"Request error for URL {req.url}: {e}")
            raise

    @property
    def BASE_URL(self):
        return "https://maps.googleapis.com/maps/api/place/{query_type}/json"
