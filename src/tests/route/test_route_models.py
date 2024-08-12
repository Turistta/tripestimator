from datetime import datetime, timedelta

import pendulum
import pytest
from pydantic import ValidationError

from models.place_models import Coordinates
from models.route_models import (
    Route,
    RouteQueryParams,
    Transportation,
    TransportationMode,
)


class TestTransportation:
    def test_valid_transportation(self):
        valid_transport = Transportation(mode=TransportationMode.CAR, fare=10.50, provider="Uber", details="Express")
        assert valid_transport.mode == TransportationMode.CAR
        assert valid_transport.fare == 10.50
        assert valid_transport.provider == "Uber"
        assert valid_transport.details == "Express"

    def test_minimal_transportation(self):
        minimal_transport = Transportation(mode=TransportationMode.WALK)  # type: ignore
        assert minimal_transport.mode == TransportationMode.WALK
        assert minimal_transport.fare is None
        assert minimal_transport.provider is None
        assert minimal_transport.details is None

    def test_invalid_provider(self):
        with pytest.raises(ValidationError):
            Transportation(mode=TransportationMode.BUS, provider="")  # type: ignore


class TestRouteQueryParams:
    @pytest.fixture
    def future_time(self):
        return pendulum.now().add(hours=8)

    @pytest.fixture
    def past_time(self):
        return pendulum.now().subtract(hours=8)

    def test_valid_query_params(self, future_time):
        valid_params = RouteQueryParams(
            origin="CnIJN1t-tDe1EmsRUsoyN13frY4",
            destination="ChIJP3Sa8ziYEmsRUKgyFmh9AQM",
            mode=TransportationMode.CAR,
            depart_at=future_time,
        )  # type: ignore
        assert valid_params.origin == "CnIJN1t-tDe1EmsRUsoyN13frY4"
        assert valid_params.destination == "ChIJP3Sa8ziYEmsRUKgyFmh9AQM"
        assert valid_params.mode == TransportationMode.CAR
        assert valid_params.depart_at > pendulum.now()  # type: ignore

    def test_past_time_validation(self, past_time):
        past_time = datetime.now() - timedelta(hours=1)
        with pytest.raises(ValidationError):
            RouteQueryParams(
                origin="CnIJN1t-tDe1EmsRUsoyN13frY4",
                destination="ChIJP3Sa8ziYEmsRUKgyFmh9AQM",
                mode=TransportationMode.CAR,
                depart_at=past_time,
            )  # type: ignore

    def test_arrive_by_before_depart_at(self, future_time):
        with pytest.raises(ValidationError):
            RouteQueryParams(
                origin="CnIJN1t-tDe1EmsRUsoyN13frY4",
                destination="ChIJP3Sa8ziYEmsRUKgyFmh9AQM",
                mode=TransportationMode.CAR,
                depart_at=future_time,
                arrive_by=pendulum.now(),  # type: ignore
            )


class TestRoute:
    @pytest.fixture
    def valid_route_data(self):
        return {
            "origin": Coordinates(latitude=1.0, longitude=1.0),
            "destination": Coordinates(latitude=2.0, longitude=2.0),
            "polyline": "fhuoFbkajWnFwBuA`GsDeB",
            "duration": 30.5,
            "distance": 5.2,
            "transportation": Transportation(mode=TransportationMode.CAR),  # type: ignore
        }

    def test_valid_route(self, valid_route_data):
        route = Route(**valid_route_data)
        assert route.origin.latitude == 1.0
        assert route.destination.longitude == 2.0
        assert route.polyline == "fhuoFbkajWnFwBuA`GsDeB"
        assert route.duration == 30.5
        assert route.distance == 5.2
        assert route.transportation.mode == TransportationMode.CAR

    def test_same_origin_destination(self, valid_route_data):
        valid_route_data["destination"] = Coordinates(latitude=1.0, longitude=1.0)
        with pytest.raises(ValidationError):
            Route(**valid_route_data)

    def test_non_positive_duration(self, valid_route_data):
        valid_route_data["duration"] = 0
        with pytest.raises(ValidationError):
            Route(**valid_route_data)

    def test_negative_distance(self, valid_route_data):
        valid_route_data["distance"] = -1
        with pytest.raises(ValidationError):
            Route(**valid_route_data)

    def test_transportation_serialization(self, valid_route_data):
        route = Route(**valid_route_data)
        serialized = route.model_dump()
        assert serialized["transportation"] == "CAR"
