import json
from json import JSONDecodeError

from models.place_models import Coordinates
from models.route_models import Route, Transportation, TransportationMode


class RouteParser:
    @staticmethod
    def parse(response: str, transportation_mode: TransportationMode) -> Route:
        try:
            response_data = json.loads(response)
            route = response_data.get("routes", [{}])[0]
            route_leg = route.get("legs", [{}])[0]

            origin = route_leg.get("startLocation", {}).get("latLng", Coordinates.model_dump)
            destination = route_leg.get("endLocation", {}).get("latLng", Coordinates.model_dump)
            polyline = route.get("polyline", {}).get("encodedPolyline", "")
            duration = float(route.get("duration", "0").replace("s", "")) / 60
            distance = route.get("distanceMeters", 0)

            _money = route.get("travelAdvisory", {}).get("transitFare", {})
            fare = float(_money.get("units", 0)) + float(_money.get("nanos", 0)) / (10**9)
            route.get
            transportation = {
                "mode": transportation_mode,
                "fare": fare,
                "provider": None,  # TODO: do something.
                "details": str(route.get("travelAdvisory", {}).get("fuelConsumptionMicroliters", "")),
            }

            return Route(
                origin=Coordinates(**origin),
                destination=Coordinates(**destination),
                polyline=polyline,
                duration=duration,
                distance=distance,
                transportation=Transportation(**transportation),
            )
        except JSONDecodeError as e:
            raise e
