from models.place_models import Location, Picture, Review, PlaceInfo, BASE_URL
from pydantic import ValidationError, SecretStr
from typing import Dict, List, Optional
from typing import TypeVar
import pendulum
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T")


class LocationParser:
    @staticmethod
    def parse_location(place: Dict) -> Location:
        """Parses location data from a place dictionary. Returns an empty Location if the data is invalid."""
        if not place.get("geometry", {}).get("location"):
            logger.warning("Location parsing error: Missing geometry or location data")
            return Location(address="", plus_code="", latitude=0.0, longitude=0.0)

        try:
            return Location(
                address=place.get("formatted_address", ""),
                plus_code=place.get("plus_code", ""),
                latitude=place["geometry"]["location"]["lat"],
                longitude=place["geometry"]["location"]["lng"],
            )
        except KeyError as e:
            logger.error(f"Location parsing error: Unexpected missing key {e} in place data: {place}")
            return Location(address="", plus_code="", latitude=0.0, longitude=0.0)


class PictureParser:
    @staticmethod
    def parse_pictures(
        pictures_data: List[Dict], api_key: Optional[str] = None, width: Optional[T] = 400
    ) -> List[Picture]:
        """Parses picture data from a list of dictionaries, optionally using api_key for photo URLs."""
        try:
            width_str = width if isinstance(width, str) else str(width)
            return [
                Picture(
                    url=(
                        f"{BASE_URL}photo?maxwidth={width_str}&photoreference={photo.get('photo_reference', '')}&key={api_key}"
                        if api_key
                        else ""
                    ),
                    width=photo.get("width", 0),
                    height=photo.get("height", 0),
                )
                for photo in pictures_data
            ]
        except KeyError as e:
            logger.error(f"Pictures parsing error: Unexpected missing key {e} in pictures data: {pictures_data}")
            return []
        except (TypeError, ValueError) as e:
            logger.error(f"Picture parsing error: {e}")
            return []


class ReviewParser:
    @staticmethod
    def parse_reviews(reviews_data: List[Dict]) -> List[Review]:
        """Parses review data from a list of dictionaries."""
        try:
            return [
                Review(
                    author_name=review.get("author_name", ""),
                    author_profile=review.get("author_url", ""),
                    language=review.get("language", ""),
                    text=review.get("text", ""),
                    rating=review.get("rating", 0.0),
                    publication_timestamp=pendulum.parse(review.get("time", ""), strict=False),
                )
                for review in reviews_data
            ]
        except (KeyError, pendulum.parsing.exceptions.ParserError) as e:
            logger.error(f"Reviews parsing error: {e} in reviews data: {reviews_data}")
            return []


class PlaceParser:
    @staticmethod
    def parse_place_info(place: Dict, api_key: Optional[str] = None) -> PlaceInfo:
        """Parses complete place information, optionally using api_key for the photo URLs."""
        try:
            pictures = PictureParser.parse_pictures(place.get("photos", []), api_key)
            location = LocationParser.parse_location(place)
            reviews = ReviewParser.parse_reviews(place.get("reviews", []))

            return PlaceInfo(
                place_id=place.get("place_id", ""),
                name=place.get("name", ""),
                location=location,
                types=place.get("types", []),
                reviews=reviews,
                pictures=pictures,
                ratings_total=place.get("user_ratings_total", 0),
                opening_hours=place.get("opening_hours", {}).get("periods", []),
            )
        except ValidationError as e:
            logger.error(f"PlaceInfo validation error: {e} in place data: {place}")
            return PlaceInfo(
                place_id="",
                name="",
                location=Location(address="", plus_code="", latitude=0.0, longitude=0.0),
                types=[],
                reviews=[],
                pictures=[],
                ratings_total=0,
                opening_hours=[],
            )
