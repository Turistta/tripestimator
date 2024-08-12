from datetime import datetime
from enum import Enum
from typing import Annotated, Optional

import pendulum
from pydantic import BaseModel, Field, ValidationInfo, field_serializer, field_validator
from pydantic_extra_types.pendulum_dt import DateTime

from .place_models import Coordinates
from .utils_models import BaseQueryParams


class TransportationMode(Enum):
    CAR = 0
    BIKE = 1
    BUS = 2
    TRAIN = 3
    WALK = 4


class Transportation(BaseModel):
    mode: Annotated[
        TransportationMode,
        Field(description="The mode of transportation", examples=["car", "bike", "bus", "train", "walk"]),
    ]
    fare: Annotated[
        Optional[float],
        Field(
            default=None,
            ge=0,
            description="The cost of the transportation, if applicable",
            examples=[10.50, 2.75, None],
        ),
    ]
    provider: Annotated[
        Optional[str],
        Field(
            default=None,
            description="The name of the transportation provider, if applicable",
            examples=["Uber", "Lyft", "Metro Transit", None],
        ),
    ]
    details: Annotated[
        Optional[str],
        Field(
            default=None,
            description="Additional details about the transportation",
            examples=["Express bus", "Shared ride", None],
        ),
    ]

    @field_validator("provider")
    @classmethod
    def provider_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v.strip() == "":
            raise ValueError("Provider cannot be an empty string")
        return v


class RouteQueryParams(BaseQueryParams):

    origin: Annotated[
        str,
        Field(
            description="The place_id of the starting point",
            examples=["CnIJN1t-tDe1EmsRUsoyN13frY4", "ThIKP3Za8ziYEmsRUKgyFmh4AQM"],
        ),
    ]
    destination: Annotated[
        str,
        Field(
            description="The place_id of the end point",
            examples=["ChIJP3Sa8ziYEmsRUKgyFmh9AQM", "YhIJN1t_tDeuEmsRUsoyG83frY4"],
        ),
    ]
    mode: Annotated[
        TransportationMode,
        Field(description="The preferred mode of transportation", examples=["car", "bike", "bus", "train", "walk"]),
    ]
    depart_at: Annotated[
        Optional[DateTime],
        Field(
            description="The desired departure time (if not provided, assumed to be now)",
            examples=["2023-06-15T14:30:00Z"],
            default=None,
        ),
    ]
    arrive_by: Annotated[
        Optional[DateTime],
        Field(
            description="The maximal arrival time.",
            examples=["2023-06-15T18:00:00Z"],
            default=None,
        ),
    ]

    @field_validator("arrive_by", "depart_at")
    @classmethod
    def validate_times(cls, v: Optional[DateTime], info: ValidationInfo) -> Optional[datetime]:
        if v is not None and v < pendulum.now():
            raise ValueError("Time cannot be in the past")
        if "arrive_by" in info.data and "depart_at" in info.data:
            if info.data["arrive_by"] is not None and info.data["depart_at"] is not None:
                if info.data["arrive_by"] <= info.data["depart_at"]:
                    raise ValueError("arrive_by must be later than depart_at")
        return v


class Route(BaseModel):
    origin: Annotated[Coordinates, Field(description="The starting point of the route")]
    destination: Annotated[Coordinates, Field(description="The end point of the route")]
    polyline: Annotated[
        str,
        Field(min_length=1, description="Encoded polyline representing the route", examples=["fhuoFbkajWnFwBuA`GsDeB"]),
    ]
    duration: Annotated[
        float, Field(gt=0, description="The estimated duration of the trip in minutes", examples=[30.5, 45.0, 120.75])
    ]
    distance: Annotated[
        float, Field(gt=0, description="The distance of the route in kilometers", examples=[5.2, 10.0, 42.3])
    ]
    transportation: Transportation

    @field_serializer("transportation")
    def serialize_transportation(self, transportation: Transportation):
        return transportation.mode.name

    @field_validator("origin", "destination")
    @classmethod
    def places_must_differ(cls, v: Coordinates, info: ValidationInfo) -> Coordinates:
        if info.field_name == "destination":
            origin = info.data.get("origin")
            if origin and origin.latitude == v.latitude and origin.longitude == v.longitude:
                raise ValueError("Origin and destination must be different")
        return v
