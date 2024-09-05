import pytest

from calculators.default_cost_calculator import DefaultCostCalculator


@pytest.fixture
def calculator():
    return DefaultCostCalculator()


@pytest.mark.parametrize(
    "distance, time_estimated, traffic_condition, fuel_price, expected_cost",
    [
        (10000, 20, 1.0, 5.55, 20.55),  # Light traffic
        (16000, 30, 1.2, 5.72, 30.98),  # Moderate traffic
        (80000, 120, 1.5, 5.86, 135.32),  # Heavy traffic
        (20000, 30, 1.2, 17.7, 62.48),  # Moderate traffic with higher fuel price
        (1000, 10, 1.5, 6.30, 10.94),  # Heavy traffic with small distance
    ],
)
def test_estimate_cost(calculator, distance, time_estimated, traffic_condition, fuel_price, expected_cost) -> None:
    calculated_cost = calculator.estimate_cost(distance, time_estimated, traffic_condition, fuel_price)
    assert calculated_cost == pytest.approx(expected_cost, 0.01)
