import logging
from typing import Dict

import requests
from pydantic import BaseModel
from requests.exceptions import HTTPError
from requests.models import PreparedRequest

BASE_URL = "https://maps.googleapis.com/maps/api/place/{query_type}/json"

logger = logging.getLogger(__name__)


class PlaceFetcher(BaseModel):
    def fetch(self, params: Dict[str]) -> str:  # type: ignore
        url = BASE_URL.format(params.pop(params._query_type))  # type: ignore
        req = PreparedRequest()
        req.prepare_url(url, params)
        try:
            response = requests.get(url=req.url)  # type: ignore
            response.raise_for_status()
            logger.info("Successfully fetched raw data.")
            return response.text
        except HTTPError as e:
            logger.error(f"Request error for URL {req.url}: {e}")
            raise
