from requests.models import PreparedRequest
from requests.exceptions import HTTPError
from pydantic import BaseModel
from typing import Dict
import logging
import requests

BASE_URL = "https://maps.googleapis.com/maps/api/place/{query_type}/json"

logger = logging.getLogger(__name__)


class PlaceFetcher(BaseModel):
    def fetch(self, params: Dict[str]) -> str:
        url = BASE_URL.format(params.pop(params._query_type))
        req = PreparedRequest()
        req.prepare_url(url, params)
        try:
            response = requests.get(req.url)
            response.raise_for_status()
            logger.info("Successfully fetched raw data.")
            return response.text
        except HTTPError as e:
            logger.error(f"Request error for URL {req.url}: {e}")
            raise
