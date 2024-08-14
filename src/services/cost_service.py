import logging

from calculators.base_cost_calculator import BaseCostCalculator
from fetchers.cost_fetcher import CostFetcher
from models.cost_models import (
    CostComponents,
    CostEstimate,
    CostEstimationParams,
    Currency,
)
from parsers.cost_parsers import CostParser

logger = logging.getLogger(__name__)


class CostService:
    def __init__(self, calculator: BaseCostCalculator, parser: CostParser, fetcher: CostFetcher) -> None:
        self.fetcher = fetcher
        self.parser = parser
        self.calculator = calculator

    def estimate_cost(self, params: CostEstimationParams) -> CostEstimate:
        logger.info("Estimating cost")

        raw_data = self.fetcher.fetch(params.state)
        fuel_price = self.parser.parse(raw_data)
        traffic_weight = self.parser.parse_traffic_condition(params.traffic_condition)
        final_cost = self.calculator.estimate_cost(
            distance=params.distance,
            time_estimated=params.time_estimated,
            traffic_weight=traffic_weight,
            fuel_price=fuel_price,
        )
        cost_components = CostComponents(
            fuel_price=fuel_price,
            traffic_adjustment=1.0,
            # traffic_adjustment=params.traffic_condition, # Fix traffic_adjustment parser.
            time_cost=self.calculator.TIME_FACTOR,
            base_cost=self.calculator.BASE_COST,
            fuel_consumption=self.calculator.FUEL_EFFICIENCY,
        )
        currency = Currency()  # Default currency (Real) # type: ignore
        logger.info(f"Estimated cost: {final_cost:.2f}")

        return CostEstimate(
            estimated_cost=final_cost,
            currency=currency,
            cost_details=cost_components,
            source_urls=self.fetcher.source_url,
        )
