import logging

import requests
from requests.exceptions import HTTPError

from fetchers.base_fetcher import BaseFetcher
from models.traffic_models import TrafficQueryParams

logger = logging.getLogger(__name__)


class TrafficFetcher(BaseFetcher):
    def fetch(self, params: TrafficQueryParams) -> str:
        return ""

    @property
    def BASE_URL(self):
        return "https://precos.petrobras.com.br/web/precos-dos-combustiveis/w/gasolina/"
