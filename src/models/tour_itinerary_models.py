from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from models.cost_models import CostEstimate
from models.place_models import PlaceInfo, PlaceQuery
from models.route_models import TransportationMode


class TourItinerary(BaseModel):
    start_point: PlaceInfo
    end_point: PlaceInfo
    departure_time: datetime
    arrival_time: datetime
    cost_estimate: CostEstimate
    transportation_method: TransportationMode

    class Config:
        arbitrary_types_allowed = True


class TourRequest(BaseModel):
    place_a: Annotated[
        PlaceQuery,
        Field(
            ...,
            description="Query for the first place. Can be NearbySearch, FindPlace, or TextSearch.",
        ),
    ]
    place_b: Annotated[
        PlaceQuery,
        Field(
            ...,
            description="Query for the second place. Can be NearbySearch, FindPlace, or TextSearch.",
        ),
    ]
    transportation_method: Annotated[
        TransportationMode,
        Field(
            ...,
            description="The mode of transportation to use.",
        ),
    ]

    class Config:
        schema_extra = {
            "examples": {
                "FindPlace Query": {
                    "summary": "FindPlace for both locations",
                    "description": "This example uses FindPlace queries for both place_a and place_b",
                    "value": {
                        "place_a": {"text_input": "Palácio Pedro Ludovico", "inputtype": "textquery"},
                        "place_b": {"text_input": "Goiania Shopping", "inputtype": "textquery"},
                        "transportation_method": "CAR",
                    },
                },
                "TextSearch Query": {
                    "summary": "TextSearch for both locations",
                    "description": "This example uses TextSearch queries for both place_a and place_b",
                    "value": {
                        "place_a": {"query": "restaurant", "radius": 1000, "location": "-16.6869,-49.2648"},
                        "place_b": {"query": "museum", "radius": 2000, "location": "-16.6869,-49.2648"},
                        "transportation_method": "BIKE",
                    },
                },
                "NearbySearch Query": {
                    "summary": "NearbySearch for both locations",
                    "description": "This example uses NearbySearch queries for both place_a and place_b",
                    "value": {
                        "place_a": {
                            "location": {"latitude": -16.6869, "longitude": -49.2648},
                            "radius": 1000,
                            "keyword": "park",
                        },
                        "place_b": {
                            "location": {"latitude": -16.6869, "longitude": -49.2648},
                            "radius": 1500,
                            "keyword": "restaurant",
                        },
                        "transportation_method": "WALK",
                    },
                },
                "Mixed Query Types": {
                    "summary": "Mixed query types for each location",
                    "description": "This example uses FindPlace for place_a and TextSearch for place_b",
                    "value": {
                        "place_a": {"text_input": "Parque Vaca Brava", "inputtype": "textquery"},
                        "place_b": {"query": "restaurant", "radius": 1000, "location": "-16.6869,-49.2648"},
                        "transportation_method": "BUS",
                    },
                },
            }
        }
