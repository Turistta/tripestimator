import json
from json import JSONDecodeError
from typing import Any, Dict, List

import pendulum
from pydantic_core import Url

from models.place_models import (
    DAYS_OF_WEEK,
    Coordinates,
    Location,
    Picture,
    PlaceInfo,
    Review,
)


class PlaceParser:
    @staticmethod
    def parse(response: str, response_type: str) -> List[PlaceInfo]:
        try:
            json_response = json.loads(response)
            if response_type == "textsearch" or response_type == "nearbysearch":
                return [PlaceParser._parse_place(place) for place in json_response.get("results", [])]
            elif response_type == "findplacefromtext":
                return [PlaceParser._parse_place(place) for place in json_response.get("candidates", [])]
            else:
                raise ValueError(f"Unknown response type: {response_type}")  # Exception treated by builder?
        except JSONDecodeError as e:
            raise e

    @staticmethod
    def _parse_place(place: Dict[str, Any]) -> PlaceInfo:
        return PlaceInfo(
            place_id=place.get("place_id", ""),
            name=place.get("name", ""),
            location=PlaceParser._parse_location(place),
            types=place.get("types", []),
            reviews=PlaceParser._parse_reviews(place.get("reviews", [])),
            pictures=PlaceParser._parse_pictures(place.get("photos", [])),
            ratings_total=place.get("user_ratings_total", 0),
            opening_hours=PlaceParser._parse_opening_hours(place.get("opening_hours", {})),
        )

    @staticmethod
    def _parse_location(place: Dict[str, Any]) -> Location:
        geometry = place.get("geometry", {})
        location = geometry.get("location", {})
        return Location(
            address=place.get("formatted_address", ""),
            plus_code=place.get("plus_code", {}).get("compound_code", ""),
            coordinates=Coordinates(latitude=location.get("lat", 0.0), longitude=location.get("lng", 0.0)),
        )

    @staticmethod
    def _parse_reviews(reviews: List[Dict[str, Any]]) -> List[Review]:
        return [
            Review(
                author_name=review.get("author_name", ""),
                author_profile=Url(review.get("author_url", "")),
                language=review.get("language", ""),
                text=review.get("text", ""),
                rating=review.get("rating", 0.0),
                publication_timestamp=pendulum.from_timestamp(review.get("time", 0)),  # type: ignore
            )  # Fix timezones from datetime - PR: https://github.com/sdispater/pendulum/pull/831
            for review in reviews
        ]

    @staticmethod
    def _parse_pictures(photos: List[Dict[str, Any]]) -> List[Picture]:
        return [
            Picture(
                url=Url(
                    f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={photo.get('width', 400)}"
                    + f"&photoreference={photo.get('photo_reference')}&key={{GOOGLE_API_KEY}}"
                ),
                width=photo.get("width", 400),
                height=photo.get("height", 400),
            )
            for photo in photos
        ]

    @staticmethod
    def _parse_opening_hours(opening_hours: Dict[str, Any]) -> Dict[str, str]:
        intervals = {}

        if opening_hours and "periods" in opening_hours:
            for period in opening_hours["periods"]:
                day_index = period["open"]["day"]
                day_name = DAYS_OF_WEEK[day_index]

                open_time = pendulum.parse(period["open"]["time"], strict=False).format("HH:mm")  # type: ignore
                close_time = pendulum.parse(period["close"]["time"], strict=False).format("HH:mm")  # type: ignore

                if close_time < open_time:
                    close_time = (
                        pendulum.parse(period["close"]["time"], strict=False)
                        .add(days=1)  # type: ignore
                        .format("HH:mm")  # type: ignore
                    )

                intervals[day_name] = f"{open_time}-{close_time}"
        for day in DAYS_OF_WEEK:
            if day not in intervals:
                intervals[day] = "Closed"
        return intervals
