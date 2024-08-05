from pydantic import BaseModel, Field, HttpUrl
from typing import List, Annotated
import pendulum


class Location(BaseModel):
    address: Annotated[str, Field(default="", description="Street address.")]
    plus_code: Annotated[str, Field(default="", description="Plus code (address code).")]
    latitude: Annotated[float, Field(description="Latitude of the location.", ge=-90.0, le=90.0)]
    longitude: Annotated[float, Field(description="Longitude of the location.", ge=-180.0, le=180.0)]


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
        pendulum.DateTime, Field(default=None, description="Timestamp of when the review was published.")
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
        List[pendulum.Interval],
        Field(
            default=[],
            min_items=7,
            description="Opening hours of the place, with at least 7 intervals (one for each day of the week).",
        ),
    ]
