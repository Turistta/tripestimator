import pytest

from models.cost_models import TRAFFIC_CONDITION_WEIGHT
from parsers.cost_parsers import CostParser


@pytest.fixture
def cost_parser():
    return CostParser()


class TestCostParser:

    def test_parse_valid(self, cost_parser):
        """Test if the method correctly parses a valid fuel price"""
        html = '<div id="telafinal-precofinal">5,67</div>'
        assert cost_parser.parse(html) == 5.67

    def test_parse_invalid_format(self, cost_parser):
        """Test if the method raises a ValueError when the price format is invalid"""
        html = '<div id="telafinal-precofinal">invalid</div>'
        with pytest.raises(ValueError, match="Failed to parse fuel price"):
            cost_parser.parse(html)

    def test_parse_missing_element(self, cost_parser):
        """Test if the method raises a ValueError when the price element is missing"""
        html = "<div>No price here</div>"
        with pytest.raises(ValueError, match="Price element not found in HTML"):
            cost_parser.parse(html)

    def test_parse_empty_html(self, cost_parser):
        """Test if the method raises a ValueError when given empty HTML"""
        with pytest.raises(ValueError, match="Failed to parse fuel price"):
            cost_parser.parse("")

    @pytest.mark.parametrize(
        "condition, expected",
        [
            ("HEAVY", TRAFFIC_CONDITION_WEIGHT["heavy"]),
            (" MOdEraTe ", TRAFFIC_CONDITION_WEIGHT["moderate"]),
            ("Light", TRAFFIC_CONDITION_WEIGHT["light"]),
        ],
    )
    def test_parse_traffic_condition_valid(self, cost_parser, condition, expected):
        """Test if the method correctly parses valid traffic conditions"""
        assert cost_parser.parse_traffic_condition(condition) == expected

    def test_parse_traffic_condition_case_insensitive(self, cost_parser):
        """Test if the method is case-insensitive when parsing traffic conditions"""
        assert cost_parser.parse_traffic_condition("HEAVY") == TRAFFIC_CONDITION_WEIGHT["heavy"]

    def test_parse_traffic_condition_unknown(self, cost_parser):
        """Test if the method raises a ValueError for unknown traffic conditions"""
        with pytest.raises(ValueError, match="Unknown traffic condition"):
            cost_parser.parse_traffic_condition("Extreme")
