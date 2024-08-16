from pydantic import ValidationError

from fetchers.route_fetcher import RouteFetcher
from models.route_models import Route, RouteQueryParams
from parsers.route_parsers import RouteParser
from services.route_service import RouteService


class RouteBuilder:
    def __init__(self):
        fetcher = RouteFetcher()
        parser = RouteParser()
        self.route_service = RouteService(fetcher, parser)

    async def build(self, **kwargs) -> Route:
        try:
            params = RouteQueryParams(**kwargs)
            return await self.route_service.get_route(params)
        except ValidationError as e:
            raise ValueError(f"Invalid route parameters: {str(e)}") from e
