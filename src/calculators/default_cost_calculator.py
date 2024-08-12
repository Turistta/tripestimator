from calculators.base_cost_calculator import BaseCostCalculator


class DefaultCostCalculator(BaseCostCalculator):

    def estimate_cost(
        self, distance_km: float, time_estimated: float, traffic_weight: float, fuel_price: float
    ) -> float:
        fuel_cost = (distance_km / self.FUEL_EFFICIENCY) * fuel_price * traffic_weight
        total_cost = self.BASE_COST + fuel_cost + ((time_estimated / 60) * self.TIME_FACTOR)
        return total_cost

    @property
    def BASE_COST(self) -> float:
        return 5.0

    @property
    def TIME_FACTOR(self) -> float:
        return 0.5

    @property
    def FUEL_EFFICIENCY(self) -> float:
        return 10.0
