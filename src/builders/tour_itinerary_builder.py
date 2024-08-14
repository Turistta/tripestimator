import pendulum

from builders.cost_builder import CostBuilder
from builders.place_builder import PlaceBuilder
from builders.route_builder import RouteBuilder
from builders.traffic_builder import TrafficBuilder
from models.route_models import Transportation
from models.tour_itinerary_models import TourItinerary


class TourItineraryBuilder:
    def __init__(self):
        self.place_builder = PlaceBuilder()
        self.route_builder = RouteBuilder()
        self.traffic_builder = TrafficBuilder()
        self.cost_builder = CostBuilder()

    def build(self, place_a: str, place_b: str, transportation_method: Transportation) -> TourItinerary:
        start_point = self.place_builder.build(place_a)  # TODO: add params type keyword # type: ignore
        end_point = self.place_builder.build(place_b)  # TODO: add params type keyword # type: ignore

        route = self.route_builder.build(  # Get route info between places
            origin=start_point.place_id,
            destination=end_point.place_id,
            mode=transportation_method.mode,
        )

        traffic_condition = self.traffic_builder.build(  # Get traffic conditions
            polyline=route.polyline, transportation_method=transportation_method
        )

        cost_estimate = self.cost_builder.build(  # Get the cost estimation
            distance=route.distance,
            time_estimated=route.duration,
            transportation_method=transportation_method,
            traffic_condition=traffic_condition,
        )

        return TourItinerary(  # Creates the "itinerary".
            start_point=start_point,
            end_point=end_point,
            departure_time=pendulum.now(),  # type: ignore
            arrival_time=pendulum.now().add(route.duration),  # type: ignore
            cost_estimate=cost_estimate,
            transportation_method=transportation_method,
        )
