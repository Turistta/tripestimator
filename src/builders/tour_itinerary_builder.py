import asyncio
from datetime import datetime, timedelta

from builders.cost_builder import CostBuilder
from builders.place_builder import PlaceBuilder
from builders.route_builder import RouteBuilder
from builders.traffic_builder import TrafficBuilder
from models.place_models import PlaceQuery, Location
from models.route_models import TransportationMode
from models.tour_itinerary_models import TourItinerary
from models.traffic_models import TrafficCondition


class TourItineraryBuilder:
    def __init__(self):
        self.place_builder = PlaceBuilder()
        self.route_builder = RouteBuilder()
        self.traffic_builder = TrafficBuilder()
        self.cost_builder = CostBuilder()

    async def build(
        self, place_a: PlaceQuery, place_b: PlaceQuery, transportation_method: TransportationMode
    ) -> TourItinerary:
        start_point, end_point = await asyncio.gather(
            self.place_builder.build(**place_a.model_dump()), self.place_builder.build(**place_b.model_dump())
        )

        route = await self.route_builder.build(
            origin=start_point.place_id,
            destination=end_point.place_id,
            mode=transportation_method,
        )
        traffic_condition = await self.traffic_builder.build(
            polyline=route.polyline, transportation_method=transportation_method
        )
        cost_estimate = await self.cost_builder.build(
            distance=route.distance,
            state=self._get_state_from_route(start_point.location.plus_code),
            time_estimated=int(route.duration),
            # TODO: #3 Fix explicit conversion
            traffic_condition=self._calculate_traffic_impact(traffic_condition),
        )

        return TourItinerary(
            start_point=start_point,
            end_point=end_point,
            departure_time=datetime.now(),
            arrival_time=datetime.now() + timedelta(seconds=route.duration),
            cost_estimate=cost_estimate,
            transportation_method=transportation_method,
        )

    def _get_state_from_route(self, plus_code) -> str:
        # TODO: #4 Implement actual logic to determine the state from the route.

        if plus_code is not None or plus_code != "":
            actual_state = plus_code[-2:]
            valid_states = {"AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", 
                            "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", 
                            "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"}
            if actual_state in valid_states:
                return actual_state
            else:
                return "BR"
        else:
            return "BR"
        

    def _calculate_traffic_impact(self, traffic_condition: TrafficCondition) -> str:
        # TODO: #5 Implement actual traffic condition calculator.
        return "moderate"
