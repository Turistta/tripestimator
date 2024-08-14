from abc import ABC, abstractmethod


class BaseCostCalculator(ABC):
    @abstractmethod
    def estimate_cost(
        self, distance: float, time_estimated: float, traffic_weight: float, fuel_price: float
    ) -> float:
        pass

    @property
    @abstractmethod
    def BASE_COST(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def TIME_FACTOR(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def FUEL_EFFICIENCY(self):
        raise NotImplementedError
