from pydantic import BaseModel
from pydantic_extra_types.pendulum_dt import DateTime

from models.cost_models import CostEstimate
from models.place_models import PlaceInfo
from models.route_models import Transportation


class TourItinerary(BaseModel):
    start_point: PlaceInfo
    end_point: PlaceInfo
    departure_time: DateTime
    arrival_time: DateTime
    cost_estimate: CostEstimate
    transportation_method: Transportation

    class Config:
        arbitrary_types_allowed = True
