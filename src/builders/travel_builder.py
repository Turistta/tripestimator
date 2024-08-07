from models import CostEstimationParams, BaseQueryParams, TravelInfo
from builders import CostBuilder, PlaceBuilder


class TravelBuilder:
    def __init__(self):
        self.cost_builder = CostBuilder()
        self.place_builder = PlaceBuilder()

    def build(self, cost_params: CostEstimationParams, place_params: BaseQueryParams) -> TravelInfo:
        cost_estimate = self.cost_builder.build(cost_params)
        places = self.place_builder.build(place_params)
        return TravelInfo(cost_estimate, places)
