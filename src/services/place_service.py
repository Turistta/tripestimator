from models.place_models import PlaceInfo, BaseQueryParams, QueryParamsFactory
from fetchers.place_fetcher import PlaceFetcher
from parsers.place_parsers import PlaceParser
from typing import List
import logging


logger = logging.getLogger(__name__)


class PlaceService:
    def __init__(self, fetcher: PlaceFetcher, parser: PlaceParser) -> None:
        self.fetcher = fetcher
        self.parser = parser

    def fetch_places(self, query_params: BaseQueryParams) -> List[PlaceInfo]:
        factory = QueryParamsFactory(query_params.model_dump())
        query_params_instance = factory.create_query_model()  # Instatiated class
        query_type = self._get_query_type(query_params_instance)
        query_params_instance._query_type = query_type  # Usage in fetcher.
        response_data = self.fetcher.fetch(query_params_instance)
        places = self.parser.parse(
            response=response_data, _response_type=query_type
        )  # Same logic, different approach.This can be simplified
        return places

    def _get_query_type(self, query_model: BaseQueryParams) -> str:
        query_type_mapping = {
            "NearbySearchQueryParams": "nearbysearch",
            "FindPlaceQueryParams": "findplacefromtext",
            "TextSearchQueryParams": "textsearch",
        }
        return query_type_mapping.get(query_model.__class__.__name__)
