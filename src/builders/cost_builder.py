from pydantic import ValidationError

from calculators.default_cost_calculator import DefaultCostCalculator
from fetchers.cost_fetcher import CostFetcher
from models.cost_models import CostEstimate, CostEstimationParams
from parsers.cost_parsers import CostParser
from services.cost_service import CostService


class CostBuilder:
    def __init__(self):
        calculator = DefaultCostCalculator()
        parser = CostParser()
        fetcher = CostFetcher()
        self.cost_service = CostService(calculator, parser, fetcher)

    def build(self, **kwargs) -> CostEstimate:
        try:
            params = CostEstimationParams(**kwargs)
            return self.cost_service.estimate_cost(params)
        except ValidationError as e:
            raise ValueError(f"Invalid cost parameters: {str(e)}") from e
