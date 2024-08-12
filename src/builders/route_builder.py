from typing import List

from fetchers.route_fetcher import RouteFetcher
from models.route_models import Route, RouteQueryParams
from parsers.route_parsers import RouteParser
from services.route_service import RouteService


class RouteBuilder:
    def __init__(self):
        fetcher = RouteFetcher()
        parser = RouteParser()
        self.route_service = RouteService(fetcher, parser)

    def build(self, params: RouteQueryParams) -> List[Route]:
        # TODO: Return actuall List, recursive calls.
        return [self.route_service.get_route(params)]
