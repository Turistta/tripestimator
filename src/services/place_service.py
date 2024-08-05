from parsers.place_parsers import PlaceParser, LocationParser, PictureParser, ReviewParser
from models.place_models import PlaceResponse, PlaceInfo, Location
from typing import Optional
from config import Config
import googlemaps
import logging

logger = logging.getLogger(__name__)


class PlaceService:
    def __init__(
        self,
        place_parser: PlaceParser,
        location_parser: LocationParser,
        picture_parser: PictureParser,
        review_parser: ReviewParser,
        api_key: str = Config.GOOGLE_MAPS_API_KEY,
    ):
        self.client = googlemaps.Client(key=api_key)
        self.place_parser = place_parser
        self.location_parser = location_parser
        self.picture_parser = picture_parser
        self.review_parser = review_parser

    def validate_place(self, place: str, api_key: Optional[str] = None) -> PlaceResponse:
        """Validates a place using Google Maps API and returns PlaceResponse."""
        try:
            geocode_result = self.client.geocode(place)
            if geocode_result:
                place_id = geocode_result[0]["place_id"]
                place_details = self.client.place(place_id=place_id)
                place_info = self.place_parser.parse_place_info(place_details["result"], api_key)
                return PlaceResponse(place_info=place_info)
            else:
                default_place_info = PlaceInfo(
                    place_id="",
                    name="",
                    location=Location(address="", plus_code="", latitude=0.0, longitude=0.0),
                    types=[],
                    reviews=[],
                    pictures=[],
                    ratings_total=0,
                    opening_hours=[],
                )
                return PlaceResponse(place_info=default_place_info)

        except googlemaps.exceptions.ApiError as e:
            logger.error(f"Google Maps API Error: {str(e)}")
            default_place_info = PlaceInfo(
                place_id="",
                name="",
                location=Location(address="", plus_code="", latitude=0.0, longitude=0.0),
                types=[],
                reviews=[],
                pictures=[],
                ratings_total=0,
                opening_hours=[],
            )
            return PlaceResponse(place_info=default_place_info)

        except Exception as e:
            logger.error(f"Error validating place: {str(e)}")
            default_place_info = PlaceInfo(
                place_id="",
                name="",
                location=Location(address="", plus_code="", latitude=0.0, longitude=0.0),
                types=[],
                reviews=[],
                pictures=[],
                ratings_total=0,
                opening_hours=[],
            )
            return PlaceResponse(place_info=default_place_info)
