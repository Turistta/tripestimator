from services.cost_service import CostService
from calculators.default_cost_calculator import DefaultCostCalculator
from parsers.cost_parsers import CostParser
from fetchers.cost_fetcher import CostFetcher
from models.cost_models import CostEstimate, CostEstimationParams


class CostBuilder:
    def __init__(self):
        calculator = DefaultCostCalculator()
        parser = CostParser()
        fetcher = CostFetcher()
        self.cost_service = CostService(calculator, parser, fetcher)

    def build(self, params: CostEstimationParams) -> CostEstimate:
        return self.cost_service.estimate_cost(params)
