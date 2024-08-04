from typing import Annotated, Dict, Optional, Literal, Union, Final, Generic
from pydantic import BaseModel, Field, field_validator
from models.utils_models import Currency

TrafficCondition = Literal["light", "moderate", "heavy"]
BASE_COST: Final = 5.0
TIME_FACTOR: Final = 0.5
FUEL_EFFICIENCY: Final = 10
TRAFFIC_CONDITION_WEIGHT: Final[Dict[str, float]] = {
    "light": 1.0,
    "moderate": 1.2,
    "heavy": 1.5,
}  # Traffic weight
BASE_URL: Final = "https://precos.petrobras.com.br/web/precos-dos-combustiveis/w/gasolina/"


class CostComponents(BaseModel):
    """The various components for calculating the total cost estimate for a **car** travel."""

    base_cost: Annotated[float, Field(default=BASE_COST, gt=0, description="Fixed minimum rate price")]

    time_cost: Annotated[
        float,
        Field(
            default=TIME_FACTOR,
            gt=0,
            le=1.0,
            description="Cost associated with time spent",
        ),
    ]
    traffic_adjustment: Annotated[
        Optional[Union[TrafficCondition, float]],
        Field(
            default=1.0,
            ge=0.1,
            le=2.0,
            description="Additional cost due to traffic conditions. It can be set as 'light', 'moderate' or 'heavy'",
        ),
    ]
    fuel_price: Annotated[Optional[float], Field(None, gt=0, description="Price of fuel")]
    fuel_consumption: Annotated[
        Optional[float],
        Field(
            default=FUEL_EFFICIENCY,
            gt=0,
            description="Fuel consumption rate (e.g. km/L)",
        ),
    ]
    traffic_description: Annotated[
        Optional[str],
        Field(
            default=None,
            min_length=1,
            max_length=255,
            description="Description of traffic conditions",
        ),
    ]

    @field_validator("traffic_adjustment", mode="plain")
    @classmethod
    def validate_traffic_adjustment(cls, value) -> float:
        """Maps and normalizes the traffic adjustment value based on its weight. Raises an error for unknown values."""
        print(f"Validating value: {value}")
        if isinstance(value, str):
            if value not in TRAFFIC_CONDITION_WEIGHT:
                raise ValueError(f"Unknown traffic condition '{value}'")
            return TRAFFIC_CONDITION_WEIGHT[value]
        elif isinstance(value, (float, int)):
            return float(value)
        raise ValueError(
            "Invalid type for traffic_adjustment. Must be one of: 'light', 'moderate', 'heavy' or a numeric value."
        )

    @field_validator("traffic_adjustment", mode="before")
    @classmethod
    def round_traffic_adjustment(cls, value) -> float | object:
        """Enforces two decimal places for the traffic adjusment value."""
        if isinstance(value, float):
            return round(value, 2)
        return value


class CostEstimate(BaseModel):
    """Represents the estimated cost and its details associated with the cost calculation."""

    source_urls: Annotated[
        Optional[str],
        Field(
            default=BASE_URL,
            description="Endpoint source for the data used for the cost calculation.",
        ),
    ]
    source_description: str = Field(default="Official Petrobrás website. The data is collected via webscrapping.")
    estimated_cost: Annotated[float, Field(gt=BASE_COST, description="Total estimated cost")]
    currency: Currency
    cost_details: CostComponents
