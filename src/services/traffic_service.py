from fetchers.traffic_fetcher import TrafficFetcher
from models.traffic_models import TrafficCondition, TrafficQueryParams
from parsers.traffic_parser import TrafficParser


class TrafficService:
    def __init__(self, parser: TrafficParser, fetcher: TrafficFetcher) -> None:
        self.parser = parser
        self.fetcher = fetcher

    async def get_traffic_condition(self, params: TrafficQueryParams) -> TrafficCondition:
        raw_data = await self.fetcher.fetch(params=params)
        return self.parser.parse(raw_data)
