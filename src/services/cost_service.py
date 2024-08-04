import logging
import requests
from typing import Optional
from models.cost_models import (
    BASE_URL,
    TRAFFIC_CONDITION_WEIGHT,
    FUEL_EFFICIENCY,
    TIME_FACTOR,
    BASE_COST,
)

from models.utils_models import Currency

from models.cost_models import CostEstimate, CostComponents
from parsers.cost_parsers import FuelPriceParser

logger = logging.getLogger(__name__)


class CostService:
    def __init__(self, fuel_price_parser: FuelPriceParser):
        self.fuel_price_parser = fuel_price_parser

    def fetch_raw_data(self, state: str) -> Optional[str]:
        url = BASE_URL + state
        try:
            logger.info(f"Fetching raw data from URL: {url}")
            response = requests.get(url)
            response.raise_for_status()
            logger.info("Successfully fetched raw data.")
            return response.text
        except requests.RequestException as e:
            logger.error(f"Request error for URL {url}: {e}")
            raise

    def estimate_cost(
        self,
        state: str,
        distance_km: float,
        time_estimated: float,
        traffic_condition: str,
    ) -> CostEstimate:
        logger.info(
            f"Estimating cost for state: {state}, distance: {distance_km} km, time:  {time_estimated}, traffic: {traffic_condition}"
        )

        raw_data = self.fetch_raw_data(state)
        fuel_price = self.fuel_price_parser.parse_fuel_price(raw_data)

        if fuel_price is None:
            logger.error("Failed to parse fuel price.")
            raise ValueError("Failed to parse fuel price.")

        if distance_km <= 0 or time_estimated <= 0:
            logger.error(f"Invalid distance or time. Distance: {distance_km}, Time: {time_estimated}")
            raise ValueError("Distance and time must be greater than zero.")

        traffic_weight = TRAFFIC_CONDITION_WEIGHT.get(traffic_condition, 1.0)
        fuel_cost = (distance_km / FUEL_EFFICIENCY) * fuel_price
        time_cost = (time_estimated / 60) * TIME_FACTOR
        final_cost = BASE_COST + (fuel_cost * traffic_weight) + time_cost

        if final_cost <= 0:
            logger.error(f"Calculated cost is non-positive: {final_cost:.2f}")
            raise ValueError("Calculated cost must be greater than zero.")

        cost_components = CostComponents(
            base_cost=BASE_COST,
            fuel_cost=fuel_cost,
            time_cost=time_cost,
            traffic_adjustment=traffic_weight,
            fuel_price=fuel_price,
            fuel_consumption=FUEL_EFFICIENCY,
            traffic_description=traffic_condition,
        )

        currency = Currency()

        logger.info(f"Estimated cost: {final_cost:.2f}")

        return CostEstimate(estimated_cost=final_cost, currency=currency, cost_details=cost_components)
