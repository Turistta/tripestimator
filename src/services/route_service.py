import logging

from fetchers.route_fetcher import RouteFetcher
from models.route_models import Route, RouteQueryParams
from parsers.route_parsers import RouteParser

logger = logging.getLogger(__name__)


class RouteService:
    def __init__(self, fetcher: RouteFetcher, parser: RouteParser) -> None:
        self.fetcher = fetcher
        self.parser = parser

    async def get_route(self, query_params: RouteQueryParams) -> Route:
        logger.info(f"Fetching route with query params: {query_params}")

        try:
            raw_data = await self.fetcher.fetch(query_params)
            logger.debug("Raw data fetched")
        except Exception as e:
            logger.error(f"Error fetching route data: {e}")
            raise

        try:
            route = self.parser.parse(raw_data, transportation_mode=query_params.mode)
            logger.info("Route parsed successfully.")
        except Exception as e:
            logger.error(f"Error parsing route data: {e}")
            raise

        logger.debug(f"Returning route: {route}")
        return route
