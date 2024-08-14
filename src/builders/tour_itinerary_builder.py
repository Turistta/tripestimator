from typing import Any

import pendulum

from builders.cost_builder import CostBuilder
from builders.place_builder import PlaceBuilder
from builders.route_builder import RouteBuilder
from builders.traffic_builder import TrafficBuilder
from models.route_models import TransportationMode
from models.tour_itinerary_models import TourItinerary


class TourItineraryBuilder:
    def __init__(self):
        self.place_builder = PlaceBuilder()
        self.route_builder = RouteBuilder()
        self.traffic_builder = TrafficBuilder()
        self.cost_builder = CostBuilder()

    def build(
        self, place_a: dict[str, Any], place_b: dict[str, Any], transportation_method: TransportationMode
    ) -> TourItinerary:
        """
        Builds a tour itinerary between two places using a specified transportation method.

        Parameters
        ----------
        place_a : dict[str, Any]
            A dictionary containing query parameters for the starting place. The structure can be one of the following:

            1. **NearbySearchQueryParams**:
                - **location** (Coordinates): Latitude and longitude (required).
                - **radius** (float): Search radius in meters (required).
                - **keyword** (str, optional): Search term.
                - **language** (str, optional): Result language code.
                - **maxprice** (int, optional): Maximum price level (0-4).
                - **minprice** (int, optional): Minimum price level (0-4).
                - **opennow** (bool, optional): Filter for currently open places.
                - **place_type** (str, optional): Specific place type.

            2. **FindPlaceQueryParams**:
                - **text_input** (str): Search text (required).
                - **inputtype** (str): Either 'textquery' or 'phonenumber' (required).
                - **fields** (str, optional): Comma-separated list of place data types.
                - **language** (str, optional): Result language code.

            3. **TextSearchQueryParams**:
                - **query** (str): Search text (required).
                - **radius** (int): Search radius in meters (required).
                - **language** (str, optional): Result language code.
                - **location** (str, optional): Latitude and longitude.
                - **maxprice** (int, optional): Maximum price level (0-4).
                - **minprice** (int, optional): Minimum price level (0-4).
                - **opennow** (bool, optional): Filter for currently open places.
                - **region** (str, optional): Region code.
                - **place_type** (str, optional): Specific place type.

        place_b : dict[str, Any]
            A dictionary containing query parameters for the ending place, structured identically to place_a.

        transportation_method : Transportation
            The mode of transportation to use. Must be one of the following values from the TransportationMode enum:
            - **TransportationMode.CAR**
            - **TransportationMode.BIKE**
            - **TransportationMode.BUS**
            - **TransportationMode.TRAIN**
            - **TransportationMode.WALK**

        Returns
        -------
        TourItinerary
            A TourItinerary object representing the planned route between place_a and place_b.

        Raises
        ------
        ValueError
            If the provided query parameters do not match any of the supported query types.
        """

        start_point = self.place_builder.build(**place_a)
        end_point = self.place_builder.build(**place_b)

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
