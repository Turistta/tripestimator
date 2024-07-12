from config import Config
import googlemaps
from travel_pb2 import RouteResponse, RouteInfo


class RouteService:
    def __init__(self):
        self.client = googlemaps.Client(key=Config.GOOGLE_MAPS_API_KEY)

    def calculate_route(self, origin, destination, transportation_method):
        try:
            directions = self.client.directions(
                origin=origin,
                destination=destination,
                mode=transportation_method,
                departure_time="now",
                alternatives=True,
                traffic_model="best_guess",
            )

            if directions:
                best_route = self._select_best_route(directions)
                route_info = self._parse_route_info(best_route, transportation_method)
                return RouteResponse(route_info=route_info)
            else:
                return RouteResponse(warnings=["No route found"])

        except googlemaps.exceptions.ApiError as e:
            return RouteResponse(warnings=[f"Google Maps API Error: {str(e)}"])
        except Exception as e:
            return RouteResponse(warnings=[f"Error calculating route: {str(e)}"])

    def _select_best_route(self, directions):
        """
        Chooses the best route based on distance, duration, and traffic conditions.
        """
        best_route = min(
            directions,
            key=lambda route: route["legs"][0]["duration_in_traffic"]["value"],
        )
        return best_route

    def _parse_route_info(self, route, transportation_method):
        leg = route["legs"][0]
        return RouteInfo(
            origin=leg["start_address"],
            destination=leg["end_address"],
            distance_km=leg["distance"]["value"] / 1000.0,
            duration=leg["duration_in_traffic"]["text"],
            duration_value=leg["duration_in_traffic"]["value"],
            transportation_method=transportation_method,
            steps=[
                step["html_instructions"] for step in leg["steps"]
            ], 
        )
