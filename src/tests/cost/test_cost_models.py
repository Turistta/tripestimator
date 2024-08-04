from typing import Callable
import pytest
from models.cost_models import (
    CostEstimate,
    CostComponents,
    BASE_COST,
    TIME_FACTOR,
    FUEL_EFFICIENCY,
    BASE_URL,
)


@pytest.fixture
def valid_cost_components():
    kwargs = {
        "base_cost": BASE_COST,
        "time_cost": TIME_FACTOR,
        "fuel_price": 5.0,
        "fuel_consumption": FUEL_EFFICIENCY,
        "traffic_adjustment": 1.0,
        "traffic_description": "Valid traffic description.",
    }
    return kwargs


def test_traffic_adjustment_valid_string_key(valid_cost_components: Callable) -> None:
    """Test that valid strings maps correctly to the weights dictionary values."""
    model_a = CostComponents(**valid_cost_components | dict(traffic_adjustment="light"))
    model_b = CostComponents(**valid_cost_components | dict(traffic_adjustment="moderate"))
    model_c = CostComponents(**valid_cost_components | dict(traffic_adjustment="heavy"))

    assert model_a.traffic_adjustment == 1.0
    assert model_b.traffic_adjustment == 1.2
    assert model_c.traffic_adjustment == 1.5


def test_traffic_adjustment_invalid_string_key(valid_cost_components: Callable) -> None:
    """Test that a invalid string maps doesn't map to the weight dictionary."""
    with pytest.raises(ValueError):
        CostComponents(**valid_cost_components | dict(traffic_adjustment="low"))


def test_traffic_adjustment_valid_numeric_value(
    valid_cost_components: Callable,
) -> None:
    """Test for a valid numeric value."""
    model = CostComponents(**valid_cost_components | dict(traffic_adjustment=1.8))

    assert model.traffic_adjustment == 1.8


def test_traffic_adjustment_round_float_value(valid_cost_components: Callable) -> None:
    """Test for rounding the float value."""
    model_a = CostComponents(**valid_cost_components | dict(traffic_adjustment=1.23456))
    model_b = CostComponents(**valid_cost_components | dict(traffic_adjustment=1.23778))

    assert model_a.traffic_adjustment == 1.23
    assert model_b.traffic_adjustment == 1.24


def test_traffic_adjustment_invalid_numeric_value() -> None:
    """Test for a invalid numeric value."""
    pass
