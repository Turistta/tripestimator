from typing import Optional

from pendulum.datetime import DateTime
from pydantic import BaseModel

from .route_models import Transportation
from .utils_models import BaseQueryParams


class TrafficQueryParams(BaseQueryParams):
    route_polyline: str
    transportation_method: Transportation
    departure_time: Optional[DateTime] = None


class TrafficCondition(BaseModel):
    pass
