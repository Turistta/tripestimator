from models.place_models import PlaceInfo, Location, Picture, Review
from parsers.place_parsers import PlaceParser
import pytest

# TODO: Add more test cases.


class TestPlaceParser:

    @pytest.fixture
    def valid_textsearch_response(self):
        """Provides a sample JSON response for textsearch type."""
        return {
            "results": [
                {
                    "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4",
                    "name": "Morrinhos",
                    "formatted_address": "Teste, Rua 02, Quadra 36, Jardim Teste",
                    "geometry": {"location": {"lat": 40.7484405, "lng": -73.9856644}},
                    "types": ["tourist_attraction", "point_of_interest", "restaurant"],
                    "user_ratings_total": 1,
                    "opening_hours": {
                        "open_now": True,
                        "periods": [
                            {
                                "open": {"day": 0, "time": "0800"},
                                "close": {"day": 0, "time": "0200"},
                            },
                        ],
                    },
                    "photos": [
                        {
                            "photo_reference": "CmRaAAAA-YL_I_M6z12Gz_2GWzz64g72e-PMcLAnr0eNDI",
                            "width": 2268,
                            "height": 4032,
                        }
                    ],
                    "reviews": [
                        {
                            "author_name": "Vitor Teste",
                            "author_url": "https://www.google.com/maps/contrib/12345678901234567893",
                            "language": "pt",
                            "text": "Vista fera demais!",
                            "rating": 5,
                            "time": 1691269200,
                        }
                    ],
                }
            ]
        }

    def test_parse_textsearch(self, valid_textsearch_response):
        """Tests parsing of textsearch response."""
        places = PlaceParser.parse(valid_textsearch_response, "textsearch")
        assert len(places) == 1
        place = places[0]

        assert isinstance(place, PlaceInfo)
        assert place.place_id == "ChIJN1t_tDeuEmsRUsoyG83frY4"
        assert place.name == "Morrinhos"
        assert isinstance(place.location, Location)
        assert isinstance(place.reviews[0], Review)
        assert isinstance(place.pictures[0], Picture)
        assert isinstance(place.opening_hours, dict) and len(place.opening_hours) == 7

    def test_parse_findplacefromtext(self):
        """Tests findplacefromtext (similar to textsearch)."""
        # ... similar test structure, use different sample data if needed

    def test_parse_nearbysearch(self):
        """Tests nearbysearch (similar to textsearch)."""
        # ... similar test structure, use different sample data if needed

    def test_parse_invalid_response_type(self):
        """Tests behavior with an unsupported response type."""
        with pytest.raises(ValueError):
            PlaceParser.parse({}, "invalid_type")

    def test_parse_empty_results(self):
        """Tests behavior when results list is empty."""
        empty_response = {"results": []}
        places = PlaceParser.parse(empty_response, "textsearch")
        assert len(places) == 0

    def test_parse_missing_fields(self):
        """Tests parsing with some optional fields missing in the response."""
        response_missing_fields = {
            "results": [
                {
                    "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4",
                    "name": "Empire State Building",
                    "geometry": {"location": {"lat": 40.7484405, "lng": -73.9856644}},
                    "types": ["tourist_attraction", "point_of_interest", "establishment"],
                }
            ]
        }
        places = PlaceParser.parse(response_missing_fields, "textsearch")
        assert len(places) == 1
        place = places[0]
        assert place.reviews == []  # Should be an empty list
        assert place.pictures == []
        assert place.opening_hours == {
            "Friday": "Closed",
            "Monday": "Closed",
            "Saturday": "Closed",
            "Sunday": "Closed",
            "Thursday": "Closed",
            "Tuesday": "Closed",
            "Wednesday": "Closed",
        }
