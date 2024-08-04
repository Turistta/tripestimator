from pydantic import BaseModel
from CostEstimate import CostEstimate


class TravelData(BaseModel):
    origin: Place
    destiny: Place
    distance: Distance
    time_estimate: TimeEstimate
    cost_estimate: CostEstimate
    transportation: Transportation




