from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, Field
from pydantic_extra_types.pendulum_dt import DateTime

from config import settings
from models.utils_models import Coordinates

from .route_models import TransportationMode
from .utils_models import BaseQueryParams, PolylineDecoder


class TrafficQueryParams(BaseQueryParams):
    api_key: str = settings.tomtom_api_key  # type: ignore
    polyline: str
    transportation_method: TransportationMode
    departure_time: Optional[DateTime] = None

    def get_bounding_boxes_coords(self, coordinates: list[Coordinates]) -> tuple[float, float, float, float]:
        points = len(coordinates)
        middle = int(points / 2)
        latitude, longitude = coordinates[middle].model_dump().values()
        delta = 0.01
        min_lat = latitude - delta
        max_lat = latitude + delta
        min_lon = longitude - delta
        max_lon = longitude + delta
        return min_lon, min_lat, max_lon, max_lat

    def get_coordinates(self) -> list[Coordinates]:
        return PolylineDecoder(self.polyline).decode_polyline()


class IncidentType(str, Enum):
    UNKNOWN = "Unknown"
    ACCIDENT = "Accident"
    FOG = "Fog"
    DANGEROUS_CONDITIONS = "Dangerous Conditions"
    RAIN = "Rain"
    ICE = "Ice"
    CONGESTION = "Congestion"
    LANE_CLOSED = "Lane Closed"
    ROAD_CLOSED = "Road Closed"
    ROAD_WORKS = "Road Works"
    WIND = "Wind"
    FLOOD = "Flood"
    VEHICLE_BREAKDOWN = "Vehicle Breakdown"


class Incident(BaseModel):
    type: IncidentType
    coordinates: Coordinates
    icon_category: int


class RoadType(str, Enum):
    MOTORWAY = "Motorway"
    TRUNK = "Trunk"
    PRIMARY = "Primary"
    SECONDARY = "Secondary"
    TERTIARY = "Tertiary"
    LOCAL = "Local"
    OTHER = "Other"


class FlowSegment(BaseModel):
    frc: str
    road_type: RoadType
    current_speed: float
    free_flow_speed: float
    confidence: float
    current_travel_time: float
    free_flow_travel_time: float
    road_closure: bool
    start_point: Coordinates
    end_point: Coordinates


class TrafficCondition(BaseModel):
    traffic_impact: Annotated[Optional[float], Field(default=1.0)]
    flow_segments: Annotated[list[FlowSegment], Field(default_factory=list)]
    incidents: Annotated[list[Incident], Field(default_factory=list)]

    class Config:
        allow_population_by_field_name = True
