import pytest

from models.place_models import Location, Picture, PlaceInfo, Review
from parsers.place_parsers import PlaceParser


class TestPlaceParser:

    @pytest.fixture
    def valid_textsearch_response(request):
        """Sample JSON response for textsearch query"""
        return """
{
  "results": [
    {
      "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4",
      "name": "Morrinhos",
      "formatted_address": "Teste, Rua 02, Quadra 36, Jardim Teste",
      "geometry": {
        "location": {
          "lat": 40.7484405,
          "lng": -73.9856644
        }
      },
      "types": [
        "tourist_attraction",
        "point_of_interest",
        "restaurant"
      ],
      "user_ratings_total": 1,
      "opening_hours": {
        "open_now": true,
        "periods": [
          {
            "open": {
              "day": 0,
              "time": "0800"
            },
            "close": {
              "day": 0,
              "time": "0200"
            }
          }
        ]
      },
      "photos": [
        {
          "photo_reference": "CmRaAAAA-YL_I_M6z12Gz_2GWzz64g72e-PMcLAnr0eNDI",
          "width": 2268,
          "height": 4032
        }
      ],
      "reviews": [
        {
          "author_name": "Vitor Teste",
          "author_url": "https://www.google.com/maps/contrib/12345678901234567893",
          "language": "pt",
          "text": "Vista fera demais!",
          "rating": 5,
          "time": 1691269200
        }
      ]
    }
  ]
}
"""

    @pytest.fixture
    def valid_findplacefromtext_response(request):
        """Sample JSON response for findplacefromtext query"""
        return """
{
  "candidates": [
    {
      "formatted_address": "San Martín 51, B6700CCU Luján, Provincia de Buenos Aires, Argentina",
      "geometry": {
        "location": {
          "lat": -34.56389,
          "lng": 59.1212854
        },
        "viewport": {
          "northeast": {
            "lat": -34.56383377010728,
            "lng": 59.12128543456332
          },
          "southwest": {
            "lat": -34.56389456632343,
            "lng": 59.12128544567865
          }
        }
      },
      "name": "Basilica de Luján",
      "opening_hours": {
        "open_now": false
      },
      "rating": 4.7
    }
  ],
  "status": "OK"
}
"""

    def test_parse_textsearch(self, valid_textsearch_response):
        """Tests parsing of textsearch response"""
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

    def test_parse_findplacefromtext(self, valid_findplacefromtext_response):
        """Tests parsing of findplacefromtext response"""
        places = PlaceParser.parse(valid_findplacefromtext_response, "findplacefromtext")
        assert len(places) == 1
        place = places[0]

        assert isinstance(place, PlaceInfo)
        assert place.name == "Basilica de Luján"
        assert isinstance(place.location, Location)
        assert place.location.address == "San Martín 51, B6700CCU Luján, Provincia de Buenos Aires, Argentina"
        assert isinstance(place.opening_hours, dict) and len(place.opening_hours) == 7

    def test_parse_invalid_response_type(self):
        """Tests behavior with an unsupported response type"""
        with pytest.raises(ValueError):
            PlaceParser.parse("", "invalid_type")

    def test_parse_empty_results(self):
        """Tests behavior when results list is empty"""
        empty_response = """{"results": []}"""
        places = PlaceParser.parse(empty_response, "textsearch")
        assert len(places) == 0

    def test_parse_missing_fields(self):
        """Tests parsing with some optional fields missing in the response."""
        response_missing_fields = """{
        "results": [
            {
                "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4",
                "name": "Empire State Building",
                "geometry": {"location": {"lat": 40.7484405, "lng": -73.9856644}},
                "types": ["tourist_attraction", "point_of_interest", "establishment"]
            }
        ]
    }"""
        places = PlaceParser.parse(response_missing_fields, "textsearch")
        assert len(places) == 1
        place = places[0]
        assert place.reviews == []
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
