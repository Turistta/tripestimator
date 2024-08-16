from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field

from config import settings


class Coordinates(BaseModel):
    latitude: Annotated[float, Field(ge=-90, le=90, description="Latitude in decimal degrees")]
    longitude: Annotated[float, Field(ge=-180, le=180, description="Longitude in decimal degrees")]


class BaseQueryParams(BaseModel):
    model_config = ConfigDict(extra="allow")

    api_key: str = settings.google_api_key  # type: ignore


class Currency(BaseModel):
    # TODO: Test post_init generated fields.
    #   Implement tests for this model fields as per default. Abnormal results from the API request.
    #   assignees: MarceloJordao01
    #   labels: enhancement, bug
    """Currency handler and parser"""

    model_config = ConfigDict(extra="forbid", strict=True)  # Enforce strict mode

    code: Annotated[
        Optional[str],
        Field(
            default=None,
            pattern=r"^[A-Z]{3}$",
            description="Currency code",
            examples=["BTC, USD"],
        ),
    ]
    symbol: Annotated[
        Optional[str],
        Field(
            default=None,
            min_length=1,
            max_length=10,
            description="Currency symbol",
            examples=["₿", "$"],
        ),
    ]
    name: Annotated[
        Optional[str],
        Field(
            default=None,
            min_length=2,
            max_length=30,
            description="Currency name",
            examples=["Bitcoin", "United States Dollar"],
        ),
    ]

    def __post_init__(self):
        any_attrs_provided = any(getattr(self, attr) is not None for attr in self.model_fields)

        if not any_attrs_provided:
            self.code = "BRL"
            self.symbol = "R$"
            self.name = "Brazilian Real"


class PolylineDecoder:
    def __init__(self, polyline: str):
        self.polyline = polyline

    @staticmethod
    def decode_single_coordinate(polyline: str, index: int) -> tuple[int, int]:
        result, shift, b = 0, 0, 0
        while True:
            b = ord(polyline[index]) - 63
            index += 1
            result |= (b & 0x1F) << shift
            shift += 5
            if b < 0x20:
                break
        return index, ~(result >> 1) if (result & 1) else (result >> 1)

    def decode_polyline(self) -> list[Coordinates]:
        """Decodes a polyline encoded string into a list of Coordinates."""
        index, lat, lng = 0, 0, 0
        coordinates = []
        while index < len(self.polyline):
            index, dlat = self.decode_single_coordinate(self.polyline, index)
            index, dlng = self.decode_single_coordinate(self.polyline, index)
            lat += dlat
            lng += dlng
            coordinates.append(Coordinates(latitude=lat / 1e5, longitude=lng / 1e5))
        return coordinates
