from datetime import datetime, timedelta
from typing import Union

from builders.cost_builder import CostBuilder
from builders.place_builder import PlaceBuilder
from builders.route_builder import RouteBuilder
from builders.traffic_builder import TrafficBuilder
from models.place_models import PlaceQuery
from models.route_models import TransportationMode
from models.tour_itinerary_models import TourItinerary


class TourItineraryBuilder:
    def __init__(self):
        self.place_builder = PlaceBuilder()
        self.route_builder = RouteBuilder()
        self.traffic_builder = TrafficBuilder()
        self.cost_builder = CostBuilder()

    def build(
        self, place_a: PlaceQuery, place_b: PlaceQuery, transportation_method: TransportationMode
    ) -> TourItinerary:
        start_point = self.place_builder.build(**place_a.model_dump())
        end_point = self.place_builder.build(**place_b.model_dump())

        route = self.route_builder.build(  # Get route info between places
            origin=start_point.place_id,
            destination=end_point.place_id,
            mode=transportation_method,
        )

        traffic_condition = self.traffic_builder.build(  # Get traffic conditions
            polyline=route.polyline, transportation_method=transportation_method
        )
        cost_estimate = self.cost_builder.build(  # Get the cost estimation
            distance=route.distance,
            state="GO",  # TODO: Route model Helper func to get state for CostEstimation?
            time_estimated=int(route.duration),  # TODO: Use helper, no explicit casting.
            traffic_condition="light",  # TODO: Adapt traffic_condition.
        )

        return TourItinerary(  # Creates the "itinerary".
            start_point=start_point,
            end_point=end_point,
            departure_time=datetime.now(),
            arrival_time=datetime.now() + timedelta(seconds=route.duration),
            cost_estimate=cost_estimate,
            transportation_method=transportation_method,
        )
