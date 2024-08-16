from pydantic import ValidationError

from fetchers.traffic_fetcher import TrafficFetcher
from models.traffic_models import TrafficCondition, TrafficQueryParams
from parsers.traffic_parser import TrafficParser
from services.traffic_service import TrafficService


class TrafficBuilder:
    def __init__(self):
        fetcher = TrafficFetcher()
        parser = TrafficParser()
        self.traffic_service = TrafficService(parser, fetcher)

    async def build(self, **kwargs) -> TrafficCondition:
        try:
            params = TrafficQueryParams(**kwargs)
            return await self.traffic_service.get_traffic_condition(params)
        except ValidationError as e:
            raise ValueError(f"Invalid traffic parameters: {str(e)}") from e
