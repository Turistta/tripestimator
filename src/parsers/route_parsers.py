import json
import logging

from pydantic import ValidationError

from models.route_models import Route, Transportation, TransportationMode
from models.utils_models import Coordinates

logger = logging.getLogger(__name__)


class RouteParser:
    @staticmethod
    def parse(response: str, transportation_mode: TransportationMode) -> Route:
        try:
            response_json = json.loads(response)
            route = response_json.get("routes", [{}])[0]
            route_leg = route.get("legs", [{}])[0]

            origin_data = route_leg.get("startLocation", {}).get("latLng")
            destination_data = route_leg.get("endLocation", {}).get("latLng")
            polyline = route.get("polyline", {}).get("encodedPolyline")

            if not origin_data or not destination_data or polyline is None:
                logger.error("Missing required fields: origin, destination, or polyline.")
                raise ValueError("Missing required fields: origin, destination, or polyline.")

            origin = Coordinates(**origin_data)
            destination = Coordinates(**destination_data)
            duration = float(route.get("duration", "0").replace("s", "")) / 60
            distance = route.get("distanceMeters", 0)

            _money = route.get("travelAdvisory", {}).get("transitFare", {})
            fare = float(_money.get("units", 0)) + float(_money.get("nanos", 0)) / (10**9)
            details = route.get("travelAdvisory", {}).get(
                "fuelConsumptionMicroliters",
            )
            if isinstance(details, str):
                try:
                    details = int(details)
                except ValueError:
                    pass
            transportation = {
                "mode": transportation_mode,
                "fare": fare,
                "provider": None,  # TODO: do something.
                "details": details,
            }

            return Route(
                origin=origin,
                destination=destination,
                polyline=polyline,
                duration=duration,
                distance=distance,
                transportation=Transportation(**transportation),
            )
        except ValidationError as e:
            raise ValueError(f"Validation error: {str(e)}")
