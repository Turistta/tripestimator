import logging
from typing import Any, Dict

import requests
from requests.exceptions import HTTPError

from fetchers.base_fetcher import BaseFetcher
from models.route_models import RouteQueryParams, TransportationMode

logger = logging.getLogger(__name__)


class RouteFetcher(BaseFetcher):

    def fetch(self, params: RouteQueryParams) -> str:
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": params.api_key,  # type: ignore
            "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline,routes.legs,"
            + "routes.travelAdvisory",
        }

        payload = self._build_payload(params)

        try:
            response = requests.post(self.BASE_URL, json=payload, headers=headers)
            response.raise_for_status()
            logger.info("Successfully fetched route data.")
            return response.text
        except HTTPError as e:
            logger.error(f"Request error for URL {self.BASE_URL}: {e}")
            raise

    def _build_payload(self, params: RouteQueryParams) -> Dict[str, Any]:
        payload = {
            "origin": {"placeId": params.origin},
            "destination": {"placeId": params.destination},
            "travelMode": self._get_travel_mode(params.mode),
            "routingPreference": "TRAFFIC_AWARE",  # Increased costs if AWARE, according to the docs.
            "computeAlternativeRoutes": False,
            "routeModifiers": {"avoidTolls": False, "avoidHighways": False, "avoidFerries": False},
            "languageCode": "pt-BR",
            "units": "METRIC",
        }

        if params.depart_at and not params.arrive_by:
            utc_time = params.depart_at.in_timezone("UTC")
            payload["departureTime"] = utc_time.format("YYYY-MM-DDTHH:mm:ssZ")
        elif params.arrive_by:
            utc_time = params.arrive_by.in_timezone("UTC")
            payload["arrivalTime"] = utc_time.format("YYYY-MM-DDTHH:mm:ssZ")

        return payload

    def _get_travel_mode(self, mode: TransportationMode) -> str:
        mode_mapping = {
            TransportationMode.CAR: "DRIVE",
            TransportationMode.BIKE: "BICYCLE",
            TransportationMode.WALK: "WALK",
            TransportationMode.BUS: "TRANSIT",
            TransportationMode.TRAIN: "TRANSIT",
        }
        return mode_mapping.get(mode, "DRIVE")

    @property
    def BASE_URL(self):
        return "https://routes.googleapis.com/directions/v2:computeRoutes"
