from services.place_service import PlaceService
from parsers.place_parsers import PlaceParser
from fetchers.place_fetcher import PlaceFetcher
from models.place_models import PlaceInfo, BaseQueryParams
from typing import List


class PlaceBuilder:
    def __init__(self):
        fetcher = PlaceFetcher
        parser = PlaceParser
        self.place_service = PlaceService(parser, fetcher)

    def build(self, params: BaseQueryParams) -> List[PlaceInfo]:
        return self.place_service.fetch_places(params)
