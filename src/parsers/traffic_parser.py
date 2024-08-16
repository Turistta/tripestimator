import json
import logging
from typing import Any

from models.traffic_models import (
    FlowSegment,
    Incident,
    IncidentType,
    RoadType,
    TrafficCondition,
)
from models.utils_models import Coordinates

logger = logging.getLogger(__name__)


class TrafficParser:
    @staticmethod
    def parse(response: str) -> TrafficCondition:
        try:
            response_json = json.loads(response)
            incidents_json = json.loads(response_json["incidents_data"])
            traffic_json = response_json.get("traffic_data", [])
            return TrafficCondition(
                traffic_impact=None,
                incidents=TrafficParser._parse_incidents(incidents_json),
                flow_segments=TrafficParser._parse_flow_segments(traffic_json),
            )
        except json.JSONDecodeError as json_e:
            logger.error(f"Failed to parse to JSON: {json_e}")
            raise json_e

    @staticmethod
    def _parse_incidents(incidents_data: dict[str, Any]) -> list[Incident]:
        incidents = incidents_data.get("incidents", [])
        return [
            Incident(
                type=IncidentType(TrafficParser._get_incident_type(inc["properties"]["iconCategory"])),
                coordinates=Coordinates(
                    latitude=inc["geometry"]["coordinates"][0][0], longitude=inc["geometry"]["coordinates"][0][1]
                ),
                icon_category=inc["properties"]["iconCategory"],
            )
            for inc in incidents
        ]

    @staticmethod
    def _parse_flow_segments(flow_data: list[str]) -> list[FlowSegment]:
        parsed_flow_data = [json.loads(data) for data in flow_data]
        return [
            FlowSegment(
                frc=data.get("flowSegmentData", {}).get("frc", ""),
                road_type=RoadType(TrafficParser._get_road_type(data.get("flowSegmentData", {}).get("frc", ""))),
                current_speed=data.get("flowSegmentData", {}).get("currentSpeed", 0),
                free_flow_speed=data.get("flowSegmentData", {}).get("freeFlowSpeed", 0),
                confidence=data.get("flowSegmentData", {}).get("confidence", 0),
                current_travel_time=data.get("flowSegmentData", {}).get("currentTravelTime", 0),
                free_flow_travel_time=data.get("flowSegmentData", {}).get("freeFlowTravelTime", 0),
                road_closure=data.get("flowSegmentData", {}).get("roadClosure", False),
                start_point=Coordinates(
                    latitude=data.get("flowSegmentData", {})
                    .get("coordinates", {})
                    .get("coordinate", [{}])[0]
                    .get("latitude", 15),
                    longitude=data.get("flowSegmentData", {})
                    .get("coordinates", {})
                    .get("coordinate", [{}])[0]
                    .get("longitude", 30),
                ),
                end_point=Coordinates(
                    latitude=data.get("flowSegmentData", {})
                    .get("coordinates", {})
                    .get("coordinate", [{}])[-1]
                    .get("latitude", 15),
                    longitude=data.get("flowSegmentData", {})
                    .get("coordinates", {})
                    .get("coordinate", [{}])[-1]
                    .get("longitude", 30),
                ),
            )
            for data in parsed_flow_data
        ]

    @staticmethod
    def _get_incident_type(ac_type):
        ac_types = {i: incident for i, incident in enumerate(IncidentType)}
        return ac_types.get(ac_type, IncidentType.UNKNOWN)

    @staticmethod
    def _get_road_type(frc: str) -> str:
        types = {
            "FRC0": RoadType.MOTORWAY,
            "FRC1": RoadType.TRUNK,
            "FRC2": RoadType.PRIMARY,
            "FRC3": RoadType.SECONDARY,
            "FRC4": RoadType.TERTIARY,
            "FRC5": RoadType.LOCAL,
            "FRC6": RoadType.LOCAL,
        }
        return types.get(frc, RoadType.OTHER)
