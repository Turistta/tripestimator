import logging

from fetchers.place_fetcher import PlaceFetcher
from models.place_models import BaseQueryParams, PlaceInfo, QueryParamsFactory
from parsers.place_parsers import PlaceParser

logger = logging.getLogger(__name__)


class PlaceService:
    def __init__(self, fetcher: PlaceFetcher, parser: PlaceParser) -> None:
        self.fetcher = fetcher
        self.parser = parser

    async def fetch_places(self, query_params: BaseQueryParams) -> PlaceInfo:

        factory = QueryParamsFactory(query_params.model_dump())
        query_params_instance = factory.create_query_model()
        query_type = self._get_query_type(query_params_instance)
        logger.debug(f"Query type determined: {query_type}")

        query_params_instance.query_type = query_type  # type: ignore
        response_data = self.fetcher.fetch(query_params_instance)
        logger.debug("Response data received.")
        places = self.parser.parse(response=response_data, response_type=query_type)
        logger.info(f"Places parsed successfully. Found {len(places)} places.")
        if not len(places):
            raise Exception("No places found!")
        return places[0]

    def _get_query_type(self, query_model: BaseQueryParams) -> str:
        query_type_mapping = {
            "NearbySearchQueryParams": "nearbysearch",
            "FindPlaceQueryParams": "findplacefromtext",
            "TextSearchQueryParams": "textsearch",
        }
        query_type = query_type_mapping.get(query_model.__class__.__name__, "")
        logger.debug(f"Mapped query model to query type: {query_type}")
        return query_type
