import logging

from fetchers.traffic_fetcher import TrafficFetcher
from models.traffic_models import TrafficCondition, TrafficQueryParams
from parsers.traffic_parser import TrafficParser


class TrafficService:
    def __init__(self, parser: TrafficParser, fetcher: TrafficFetcher) -> None:
        self.parser = TrafficParser
        self.fetcher = TrafficFetcher

    def get_traffic_condition(self, params: TrafficQueryParams) -> TrafficCondition:
        raw_data = self.fetcher.fetch(params)
        return TrafficCondition(**raw_data)
