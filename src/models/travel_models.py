from pydantic import BaseModel
from pydantic_extra_types.pendulum_dt import DateTime

from models.cost_models import CostEstimate
from models.place_models import PlaceInfo 


class TravelInfo(BaseModel):
    start_point: PlaceInfo
    end_point: PlaceInfo
    departure_time: DateTime
    arrival_time: DateTime
    # time_estimate: TimeEstimate
    # distance: Distance
    cost_estimate: CostEstimate
    transportation_method: Transportation

    class Config:
        arbitrary_types_allowed = True
