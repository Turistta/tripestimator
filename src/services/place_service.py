from config import Config
import googlemaps
from travel_pb2 import PlaceResponse, PlaceInfo, Review, Picture


class PlaceService:
    def __init__(self):
        self.client = googlemaps.Client(key=Config.GOOGLE_MAPS_API_KEY)

    def validate_place(self, place):
        try:
            geocode_result = self.client.geocode(place)
            if geocode_result:
                place_id = geocode_result[0]["place_id"]
                place_details = self.client.place(place_id=place_id)
                place_info = self._parse_place_info(place_details["result"])
                return PlaceResponse(place_info=place_info)
            else:
                return PlaceResponse(warnings=["Place not found"])

        except googlemaps.exceptions.ApiError as e:
            return PlaceResponse(warnings=[f"Google Maps API Error: {str(e)}"])
        except Exception as e:
            return PlaceResponse(warnings=[f"Error validating place: {str(e)}"])

    def _parse_place_info(self, place):
        reviews = [
            Review(
                author_name=review.get("author_name", ""),
                text=review.get("text", ""),
                rating=review.get("rating", 0.0),
                relative_time_description=review.get("relative_time_description", ""),
            )
            for review in place.get("reviews", [])
        ]

        pictures = [
            Picture(
                url=photo.get("photo_reference", ""),
                width=photo.get("width", 0),
                height=photo.get("height", 0),
            )
            for photo in place.get("photos", [])
        ]

        return PlaceInfo(
            address=place.get("formatted_address", ""),
            latitude=place["geometry"]["location"]["lat"],
            longitude=place["geometry"]["location"]["lng"],
            place_id=place["place_id"],
            name=place.get("name", ""),
            types=place.get("types", []),
            reviews=reviews,
            pictures=pictures,
        )
