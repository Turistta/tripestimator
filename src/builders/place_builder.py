from typing import List

from fetchers.place_fetcher import PlaceFetcher
from models.place_models import BaseQueryParams, PlaceInfo
from parsers.place_parsers import PlaceParser
from services.place_service import PlaceService


class PlaceBuilder:
    def __init__(self):
        fetcher = PlaceFetcher()
        parser = PlaceParser()
        self.place_service = PlaceService(fetcher, parser)

    def build(self, params: BaseQueryParams) -> List[PlaceInfo]:
        return self.place_service.fetch_places(params)
