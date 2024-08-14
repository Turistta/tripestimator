from datetime import datetime

from pydantic import BaseModel

from models.cost_models import CostEstimate
from models.place_models import PlaceInfo
from models.route_models import TransportationMode


class TourItinerary(BaseModel):
    start_point: PlaceInfo
    end_point: PlaceInfo
    departure_time: datetime
    arrival_time: datetime
    cost_estimate: CostEstimate
    transportation_method: TransportationMode

    class Config:
        arbitrary_types_allowed = True
