from abc import ABC, abstractmethod


class BaseCostCalculator(ABC):
    @abstractmethod
    def estimate_cost(
        self, distance_km: float, time_estimated: float, traffic_weight: float, fuel_price: float
    ) -> float:
        pass
