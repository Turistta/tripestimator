from calculators.base_cost_calculator import BaseCostCalculator
from typing import Final, Dict

BASE_COST: Final = 5.0
TIME_FACTOR: Final = 0.5
FUEL_EFFICIENCY: Final = 10


class DefaultCostCalculator(BaseCostCalculator):
    def estimate_cost(
        self, distance_km: float, time_estimated: float, traffic_weight: float, fuel_price: float
    ) -> float:
        fuel_cost = (distance_km / FUEL_EFFICIENCY) * fuel_price * traffic_weight
        total_cost = BASE_COST + fuel_cost + ((time_estimated / 60) * TIME_FACTOR)
        return total_cost
