import logging
from travel_pb2 import TrafficResponse, TimeEstimate
import requests
import re

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TrafficService:
    WAZE_URL = "https://www.waze.com/"
    HEADERS = {
        "User-Agent": "Mozilla/5.0",
        "referer": WAZE_URL,
    }
    VEHICLE_TYPES = ("TAXI", "MOTORCYCLE")
    COORD_MATCH = re.compile(
        r"^([-+]?)([\d]{1,2})(((\.)(\d+)(,)))(\s*)(([-+]?)([\d]{1,3})((\.)(\d+))?)$"
    )
    ROUTING_SERVER = "row-RoutingManager/routingRequest"

    def __init__(self):
        pass

    def setup(
        self,
        start_coords,
        end_coords,
        vehicle_type="",
        avoid_toll_roads=False,
        avoid_subscription_roads=False,
        avoid_ferries=False,
    ):
        self.vehicle_type = ""
        if vehicle_type and vehicle_type in self.VEHICLE_TYPES:
            self.vehicle_type = vehicle_type.upper()
        self.ROUTE_OPTIONS = {
            "AVOID_TRAILS": "t",
            "AVOID_TOLL_ROADS": "t" if avoid_toll_roads else "f",
            "AVOID_FERRIES": "t" if avoid_ferries else "f",
        }
        self.avoid_subscription_roads = avoid_subscription_roads
        if self.already_coords(start_coords):
            self.start_coords = self.coords_string_parser(start_coords)
        else:
            raise ValueError("Start address must be coordinates")
        if self.already_coords(end_coords):
            self.end_coords = self.coords_string_parser(end_coords)
        else:
            raise ValueError("End address must be coordinates")

    def already_coords(self, address):
        m = re.search(self.COORD_MATCH, address)
        return m is not None

    def coords_string_parser(self, coords):
        lat, lon = coords.split(",")
        return {"lat": lat.strip(), "lon": lon.strip(), "bounds": {}}

    def get_route(self, npaths=1, time_delta=0):
        url_options = {
            "from": "x:%s y:%s" % (self.start_coords["lon"], self.start_coords["lat"]),
            "to": "x:%s y:%s" % (self.end_coords["lon"], self.end_coords["lat"]),
            "at": time_delta,
            "returnJSON": "true",
            "returnGeometries": "true",
            "returnInstructions": "true",
            "timeout": 6000,
            "nPaths": npaths,
            "options": ",".join(
                "%s:%s" % (opt, value) for (opt, value) in self.ROUTE_OPTIONS.items()
            ),
        }
        if self.vehicle_type:
            url_options["vehicleType"] = self.vehicle_type
        if not self.avoid_subscription_roads:
            url_options["subscription"] = "*"

        response = requests.get(
            self.WAZE_URL + self.ROUTING_SERVER,
            params=url_options,
            headers=self.HEADERS,
        )
        response.encoding = "utf-8"
        return self._check_response(response)

    @staticmethod
    def _check_response(response):
        if response.ok:
            try:
                return response.json()
            except ValueError:
                return None
        return None

    def _add_up_route(self, results, real_time=True, stop_at_bounds=False):
        start_bounds = self.start_coords["bounds"]
        end_bounds = self.end_coords["bounds"]

        def between(target, min_val, max_val):
            return min_val < target < max_val

        total_time = 0
        total_free_flow_time = 0
        total_length = 0
        traffic_conditions = []

        for segment in results:
            if stop_at_bounds and segment.get("path"):
                x = segment["path"]["x"]
                y = segment["path"]["y"]
                if (
                    between(
                        x, start_bounds.get("left", 0), start_bounds.get("right", 0)
                    )
                    or between(x, end_bounds.get("left", 0), end_bounds.get("right", 0))
                ) and (
                    between(
                        y, start_bounds.get("bottom", 0), start_bounds.get("top", 0)
                    )
                    or between(y, end_bounds.get("bottom", 0), end_bounds.get("top", 0))
                ):
                    continue

            if "crossTime" in segment:
                total_time += segment[
                    "crossTime" if real_time else "crossTimeWithoutRealTime"
                ]
                total_free_flow_time += segment["crossTimeFreeFlow"]
            else:
                total_time += segment[
                    "cross_time" if real_time else "cross_time_without_real_time"
                ]
                total_free_flow_time += segment["cross_time_free_flow"]

            total_length += segment["length"]

        if len(results) > 0:
            avg_time = total_time / len(results)
            avg_free_flow_time = total_free_flow_time / len(results)
            percentage_difference = ((avg_free_flow_time - avg_time) / avg_time) * 100
        else:
            avg_time = 0
            avg_free_flow_time = 0
            percentage_difference = 0

        route_time = avg_time / 60.0
        route_distance = total_length / 1000.0
        traffic_condition = round(percentage_difference, 3)

        return route_time, route_distance, traffic_condition

    def calc_route_info(self, real_time=True, stop_at_bounds=False, time_delta=0):
        warnings = []
        try:
            route = self.get_route(1, time_delta)
            if route:
                results = route.get("response", None).get("results", None)
                route_time, route_distance, traffic_condition = self._add_up_route(
                    results, real_time=real_time, stop_at_bounds=stop_at_bounds
                )
                return TrafficResponse(
                    time_estimate=TimeEstimate(
                        distance=route_distance,
                        estimated_time=int(route_time),
                        traffic_condition=traffic_condition,
                    ),
                    warnings=warnings,
                )
            else:
                warnings.append("Empty response from Waze")
                return TrafficResponse(
                    time_estimate=TimeEstimate(
                        distance=0.0,
                        estimated_time=0,
                        traffic_condition="Unknown",
                    ),
                    warnings=warnings,
                )
        except ValueError as e:
            warnings.append(str(e))
            return TrafficResponse(
                time_estimate=TimeEstimate(
                    distance=0.0,
                    estimated_time=0,
                    traffic_condition="Unknown",
                ),
                warnings=warnings,
            )
        except Exception as e:
            warnings.append("An unexpected error occurred: " + str(e))
            return TrafficResponse(
                time_estimate=TimeEstimate(
                    distance=0.0,
                    estimated_time=0,
                    traffic_condition="Unknown",
                ),
                warnings=warnings,
            )
