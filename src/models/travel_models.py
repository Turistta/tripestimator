from pydantic import BaseModel
from models.cost_models import CostEstimate


class TravelData(BaseModel):
    origin: PlaceInfo
    destiny: PlaceInfo
    distance: Distance
    time_estimate: TimeEstimate
    cost_estimate: CostEstimate
    transportation: Transportation
