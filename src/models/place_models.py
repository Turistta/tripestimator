from typing import Annotated, Dict, Final, List, Literal, Optional

import pendulum
from pydantic import BaseModel, Field, HttpUrl, ValidationError
from pydantic_extra_types.pendulum_dt import DateTime
from .utils_models import BaseQueryParams

DAYS_OF_WEEK: Final = [pendulum.from_timestamp(0).add(days=i).format("dddd") for i in range(7)]


class Coordinates(BaseModel):
    latitude: Annotated[float, Field(ge=-90, le=90, description="Latitude in decimal degrees")]
    longitude: Annotated[float, Field(ge=-180, le=180, description="Longitude in decimal degrees")]


class NearbySearchQueryParams(BaseQueryParams):
    location: Annotated[
        Coordinates,
        Field(
            ...,
            description="Latitude and longitude where to retrieve place information.",
            examples=[{"latitude": 40.7128, "longitude": -74.0060}],
        ),
    ]
    radius: Annotated[
        float,
        Field(..., description="Distance (in meters) within which to return place results."),
    ]
    keyword: Annotated[
        Optional[str],
        Field(
            None,
            description="The text string on which to search.",
            examples=["restaurant", "Goiânia"],
        ),
    ]
    language: Annotated[
        Optional[str],
        Field(None, description="The language in which to return results.", examples=["pt", "en"]),
    ]
    maxprice: Annotated[
        Optional[int],
        Field(
            None,
            ge=0,
            le=4,
            description="Restricts results to only those places within the specified maximum price range. Values range"
            + " from 0 (most affordable) to 4 (most expensive).",
        ),
    ]
    minprice: Annotated[
        Optional[int],
        Field(
            None,
            ge=0,
            le=4,
            description="Restricts results to only those places within the specified minimum price range. Values range"
            + " from 0 (most affordable) to 4 (most expensive).",
        ),
    ]
    opennow: Annotated[
        Optional[bool],
        Field(None, description="Returns only those places that are open for business at the time the query is sent."),
    ]
    place_type: Annotated[
        Optional[str],
        Field(
            None,
            description="Restricts results to places matching the specified type.",
            examples=["restaurant", "hospital"],
        ),
    ]


class FindPlaceQueryParams(BaseQueryParams):
    text_input: Annotated[
        str,
        Field(
            ...,
            description="The text string on which to search.",
            examples=["restaurant", "123 Main Street"],
        ),
    ]
    inputtype: Annotated[
        Literal["textquery", "phonenumber"],
        Field(
            ...,
            description="The type of input. Can be either 'textquery' or 'phonenumber'.",
            examples=["textquery", "phonenumber"],
        ),
    ]
    fields: Annotated[
        Optional[str],
        Field(
            None,
            description="A comma-separated list of place data types to return.",
            examples=["formatted_address,name", "opening_hours,geometry"],
        ),
    ]

    language: Annotated[
        Optional[str],
        Field(
            None,
            description="The language in which to return results.",
            examples=["pt", "en"],
        ),
    ]


class TextSearchQueryParams(BaseQueryParams):
    query: Annotated[
        str,
        Field(
            ...,
            description="The text string on which to search.",
            examples=["restaurant", "123 Main Street"],
        ),
    ]
    radius: Annotated[
        int,
        Field(..., description="Distance (in meters) within which to return place results."),
    ]
    language: Annotated[
        Optional[str],
        Field(
            None,
            description="The language in which to return results.",
            examples=["pt", "en"],
        ),
    ]
    location: Annotated[
        Optional[str],
        Field(
            None,
            description="The point around which to retrieve place information.",
            examples=["37.7749,-122.4194"],
        ),
    ]

    maxprice: Annotated[
        int,
        Field(
            None,
            ge=0,
            le=4,
            description="Restricts results to only those places within the specified maximum price range. Values range"
            + " from 0 (most affordable) to 4 (most expensive).",
            examples=[0, 2, 4],
        ),
    ]

    minprice: Annotated[
        Optional[int],
        Field(
            None,
            ge=0,
            le=4,
            description="Restricts results to only those places within the specified minimum price range. Values range"
            + " from 0 (most affordable) to 4 (most expensive).",
            examples=[0, 1, 3],
        ),
    ]

    opennow: Annotated[
        Optional[bool],
        Field(
            None,
            description="Returns only those places that are open for business at the time the query is sent.",
        ),
    ]

    region: Annotated[
        Optional[str],
        Field(
            None,
            description="The region code.",
            examples=["br", "us"],
        ),
    ]

    place_type: Annotated[
        Optional[str],
        Field(
            None,
            description="Restricts the results to places matching the specified type.",
            examples=["restaurant", "hospital"],
        ),
    ]


class QueryParamsFactory:
    def __init__(self, query_params: Dict[str, str]):
        self.params = query_params
        self.query_params_class = self._determine_query_params_class()

    def _determine_query_params_class(self) -> type[BaseQueryParams]:
        if not self.params:
            raise ValueError("Invalid parameters: Empty query")
        if set(self.params).issubset(NearbySearchQueryParams.model_fields.keys()):
            return NearbySearchQueryParams
        if set(self.params).issubset(FindPlaceQueryParams.model_fields.keys()):
            return FindPlaceQueryParams
        if set(self.params).issubset(TextSearchQueryParams.model_fields.keys()):
            return TextSearchQueryParams
        else:
            raise ValueError("Invalid parameters: Cannot determine query type")

    def create_query_model(self) -> BaseQueryParams:
        try:
            return self.query_params_class(**self.params)
        except ValidationError as e:
            raise ValueError(f"Invalid parameters: {e}")


class Location(BaseModel):
    address: Annotated[str, Field(default="", description="Street address.")]
    plus_code: Annotated[str, Field(default="", description="Plus code (address code).")]
    coordinates: Annotated[
        Coordinates,
        Field(
            ...,
            description="Latitude and longitude where to retrieve place information.",
            examples=[{"latitude": 40.7128, "longitude": -74.0060}],
        ),
    ]


class Picture(BaseModel):
    url: Annotated[HttpUrl, Field(description="URL of the photo.")]
    width: Annotated[int, Field(description="Width of the photo in pixels.", gt=0)]
    height: Annotated[int, Field(description="Height of the photo in pixels.", gt=0)]


class Review(BaseModel):
    author_name: Annotated[str, Field(default="", description="Name of the review author.")]
    author_profile: Annotated[HttpUrl, Field(description="URL of the author's profile.")]
    language: Annotated[str, Field(default="", description="Language in which the review is written.")]
    text: Annotated[str, Field(default="", description="Text content of the review.")]
    rating: Annotated[
        float, Field(default=0.0, description="Rating given in the review, between 0.0 and 5.0.", ge=0.0, le=5.0)
    ]
    publication_timestamp: Annotated[
        DateTime, Field(default=None, description="Timestamp of when the review was published.")
    ]


class PlaceInfo(BaseModel):
    place_id: Annotated[str, Field(description="Unique identifier for the place.")]
    name: Annotated[str, Field(default="", description="Name of the place.")]
    location: Annotated[Location, Field(description="Location details of the place.")]
    types: Annotated[List[str], Field(default=[], description="Types or categories of the place.")]
    reviews: Annotated[List[Review], Field(default=[], description="List of reviews for the place.")]
    pictures: Annotated[List[Picture], Field(default=[], description="List of pictures for the place.")]
    ratings_total: Annotated[int, Field(description="Total number of ratings.", ge=0)]
    opening_hours: Annotated[
        Dict[str, str],
        Field(
            default_factory=lambda: {day: "Closed" for day in DAYS_OF_WEEK},
            description="Opening hours of the place, with day names as keys (e.g., 'Monday': '09:00-17:00').",
        ),
    ]
