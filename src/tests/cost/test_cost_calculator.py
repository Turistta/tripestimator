import pytest

from calculators.default_cost_calculator import DefaultCostCalculator


@pytest.fixture
def calculator():
    return DefaultCostCalculator()


@pytest.mark.parametrize(
    "distance, time_estimated, traffic_condition, fuel_price, expected_cost",
    [
        (10, 20, 1.0, 5.55, 10.71),  # Light traffic
        (16, 30, 1.2, 5.72, 16.23),  # Moderate traffic
        (100, 120, 0.5, 5.86, 35.30),  # Heavy traffic
        (20, 30, 1.2, 17.7, 47.73),  # Moderate traffic with higher fuel price
        (0, 10, 1.8, 6.30, 5.08),  # Heavy traffic with small distance
    ],
)
def test_estimate_cost(calculator, distance, time_estimated, traffic_condition, fuel_price, expected_cost) -> None:
    calculated_cost = calculator.estimate_cost(distance, time_estimated, traffic_condition, fuel_price)
    assert calculated_cost == pytest.approx(expected_cost, 0.01)
