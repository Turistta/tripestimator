from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TravelRequest(_message.Message):
    __slots__ = ("origin", "destination", "transportation_method", "departure_time")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    TRANSPORTATION_METHOD_FIELD_NUMBER: _ClassVar[int]
    DEPARTURE_TIME_FIELD_NUMBER: _ClassVar[int]
    origin: str
    destination: str
    transportation_method: str
    departure_time: str
    def __init__(self, origin: _Optional[str] = ..., destination: _Optional[str] = ..., transportation_method: _Optional[str] = ..., departure_time: _Optional[str] = ...) -> None: ...

class TravelResponse(_message.Message):
    __slots__ = ("route_info", "time_estimate", "cost_estimate", "warnings")
    ROUTE_INFO_FIELD_NUMBER: _ClassVar[int]
    TIME_ESTIMATE_FIELD_NUMBER: _ClassVar[int]
    COST_ESTIMATE_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    route_info: RouteInfo
    time_estimate: TimeEstimate
    cost_estimate: CostEstimate
    warnings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, route_info: _Optional[_Union[RouteInfo, _Mapping]] = ..., time_estimate: _Optional[_Union[TimeEstimate, _Mapping]] = ..., cost_estimate: _Optional[_Union[CostEstimate, _Mapping]] = ..., warnings: _Optional[_Iterable[str]] = ...) -> None: ...

class PlaceRequest(_message.Message):
    __slots__ = ("place",)
    PLACE_FIELD_NUMBER: _ClassVar[int]
    place: str
    def __init__(self, place: _Optional[str] = ...) -> None: ...

class PlaceResponse(_message.Message):
    __slots__ = ("place_info", "warnings")
    PLACE_INFO_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    place_info: PlaceInfo
    warnings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, place_info: _Optional[_Union[PlaceInfo, _Mapping]] = ..., warnings: _Optional[_Iterable[str]] = ...) -> None: ...

class PlaceInfo(_message.Message):
    __slots__ = ("address", "latitude", "longitude", "place_id", "name", "types", "reviews", "pictures")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    PLACE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    REVIEWS_FIELD_NUMBER: _ClassVar[int]
    PICTURES_FIELD_NUMBER: _ClassVar[int]
    address: str
    latitude: float
    longitude: float
    place_id: str
    name: str
    types: _containers.RepeatedScalarFieldContainer[str]
    reviews: _containers.RepeatedCompositeFieldContainer[Review]
    pictures: _containers.RepeatedCompositeFieldContainer[Picture]
    def __init__(self, address: _Optional[str] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., place_id: _Optional[str] = ..., name: _Optional[str] = ..., types: _Optional[_Iterable[str]] = ..., reviews: _Optional[_Iterable[_Union[Review, _Mapping]]] = ..., pictures: _Optional[_Iterable[_Union[Picture, _Mapping]]] = ...) -> None: ...

class Review(_message.Message):
    __slots__ = ("author_name", "text", "rating", "relative_time_description")
    AUTHOR_NAME_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_TIME_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    author_name: str
    text: str
    rating: float
    relative_time_description: str
    def __init__(self, author_name: _Optional[str] = ..., text: _Optional[str] = ..., rating: _Optional[float] = ..., relative_time_description: _Optional[str] = ...) -> None: ...

class Picture(_message.Message):
    __slots__ = ("url", "width", "height")
    URL_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    url: str
    width: int
    height: int
    def __init__(self, url: _Optional[str] = ..., width: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...

class RouteRequest(_message.Message):
    __slots__ = ("origin", "destination", "transportation_method")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    TRANSPORTATION_METHOD_FIELD_NUMBER: _ClassVar[int]
    origin: str
    destination: str
    transportation_method: str
    def __init__(self, origin: _Optional[str] = ..., destination: _Optional[str] = ..., transportation_method: _Optional[str] = ...) -> None: ...

class RouteResponse(_message.Message):
    __slots__ = ("route_info", "warnings")
    ROUTE_INFO_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    route_info: RouteInfo
    warnings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, route_info: _Optional[_Union[RouteInfo, _Mapping]] = ..., warnings: _Optional[_Iterable[str]] = ...) -> None: ...

class TrafficRequest(_message.Message):
    __slots__ = ("start_coords", "end_coords", "vehicle_type", "avoid_toll_roads", "avoid_subscription_roads", "avoid_ferries")
    START_COORDS_FIELD_NUMBER: _ClassVar[int]
    END_COORDS_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_TYPE_FIELD_NUMBER: _ClassVar[int]
    AVOID_TOLL_ROADS_FIELD_NUMBER: _ClassVar[int]
    AVOID_SUBSCRIPTION_ROADS_FIELD_NUMBER: _ClassVar[int]
    AVOID_FERRIES_FIELD_NUMBER: _ClassVar[int]
    start_coords: str
    end_coords: str
    vehicle_type: str
    avoid_toll_roads: bool
    avoid_subscription_roads: bool
    avoid_ferries: bool
    def __init__(self, start_coords: _Optional[str] = ..., end_coords: _Optional[str] = ..., vehicle_type: _Optional[str] = ..., avoid_toll_roads: bool = ..., avoid_subscription_roads: bool = ..., avoid_ferries: bool = ...) -> None: ...

class TrafficResponse(_message.Message):
    __slots__ = ("time_estimate", "warnings")
    TIME_ESTIMATE_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    time_estimate: TimeEstimate
    warnings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, time_estimate: _Optional[_Union[TimeEstimate, _Mapping]] = ..., warnings: _Optional[_Iterable[str]] = ...) -> None: ...

class CostRequest(_message.Message):
    __slots__ = ("state", "distance_km", "time_estimated", "traffic_condition")
    STATE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_KM_FIELD_NUMBER: _ClassVar[int]
    TIME_ESTIMATED_FIELD_NUMBER: _ClassVar[int]
    TRAFFIC_CONDITION_FIELD_NUMBER: _ClassVar[int]
    state: str
    distance_km: float
    time_estimated: int
    traffic_condition: str
    def __init__(self, state: _Optional[str] = ..., distance_km: _Optional[float] = ..., time_estimated: _Optional[int] = ..., traffic_condition: _Optional[str] = ...) -> None: ...

class CostResponse(_message.Message):
    __slots__ = ("cost_estimate", "warnings")
    COST_ESTIMATE_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    cost_estimate: CostEstimate
    warnings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, cost_estimate: _Optional[_Union[CostEstimate, _Mapping]] = ..., warnings: _Optional[_Iterable[str]] = ...) -> None: ...

class RouteInfo(_message.Message):
    __slots__ = ("origin", "destination", "distance_km", "duration", "duration_value", "transportation_method", "steps")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_KM_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    DURATION_VALUE_FIELD_NUMBER: _ClassVar[int]
    TRANSPORTATION_METHOD_FIELD_NUMBER: _ClassVar[int]
    STEPS_FIELD_NUMBER: _ClassVar[int]
    origin: str
    destination: str
    distance_km: float
    duration: str
    duration_value: int
    transportation_method: str
    steps: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, origin: _Optional[str] = ..., destination: _Optional[str] = ..., distance_km: _Optional[float] = ..., duration: _Optional[str] = ..., duration_value: _Optional[int] = ..., transportation_method: _Optional[str] = ..., steps: _Optional[_Iterable[str]] = ...) -> None: ...

class TimeEstimate(_message.Message):
    __slots__ = ("distance", "estimated_time", "traffic_condition")
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_TIME_FIELD_NUMBER: _ClassVar[int]
    TRAFFIC_CONDITION_FIELD_NUMBER: _ClassVar[int]
    distance: float
    estimated_time: int
    traffic_condition: float
    def __init__(self, distance: _Optional[float] = ..., estimated_time: _Optional[int] = ..., traffic_condition: _Optional[float] = ...) -> None: ...

class CostEstimate(_message.Message):
    __slots__ = ("estimated_cost",)
    ESTIMATED_COST_FIELD_NUMBER: _ClassVar[int]
    estimated_cost: float
    def __init__(self, estimated_cost: _Optional[float] = ...) -> None: ...
