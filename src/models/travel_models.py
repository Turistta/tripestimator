from pydantic import BaseModel
from models.place_models import PlaceInfo
from models.cost_models import CostEstimate


class TravelInfo(BaseModel):
    origin: PlaceInfo
    destiny: PlaceInfo
    # distance: Distance
    # time_estimate: TimeEstimate
    cost_estimate: CostEstimate
    # transportation: Transportation

    class Config:
        arbitrary_types_allowed = True
