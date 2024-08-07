from models.cost_models import CostEstimate, CostEstimationParams, CostComponents, Currency
from calculators.base_cost_calculator import BaseCostCalculator
from fetchers.cost_fetcher import CostFetcher
from parsers.cost_parsers import CostParser
import logging

logger = logging.getLogger(__name__)


class CostService:
    def __init__(self, calculator: BaseCostCalculator, parser: CostParser, fetcher: CostFetcher) -> None:
        self.fetcher = fetcher
        self.parser = parser
        self.calculator = calculator

    def estimate_cost(self, params: CostEstimationParams) -> CostEstimate:
        logger.info(
            f"Estimating cost for state: {params.state}, distance: {params.distance_km} km, "
            f"time: {params.time_estimated}, traffic: {params.traffic_condition}"
        )

        raw_data = self.fetcher.fetch(params.state)
        fuel_price = self.parser.parse(raw_data)
        traffic_weight = self.parser.parse_traffic_condition(params.traffic_condition)

        final_cost = self.calculator.estimate_cost(
            distance_km=params.distance_km,
            time_estimated=params.time_estimated,
            traffic_weight=traffic_weight,
            fuel_price=fuel_price,
        )

        cost_components = CostComponents(
            fuel_price=fuel_price,
            traffic_adjustment=params.traffic_condition,
        )

        currency = Currency()  # Default currency (Real)
        logger.info(f"Estimated cost: {final_cost:.2f}")

        return CostEstimate(estimated_cost=final_cost, currency=currency, cost_details=cost_components)
