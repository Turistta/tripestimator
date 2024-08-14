from typing import Optional

from pydantic import BaseModel
from pydantic_extra_types.pendulum_dt import DateTime

from .route_models import Transportation
from .utils_models import BaseQueryParams


class TrafficQueryParams(BaseQueryParams):
    route_polyline: str
    transportation_method: Transportation
    departure_time: Optional[DateTime] = None


class TrafficCondition(BaseModel):
    pass
