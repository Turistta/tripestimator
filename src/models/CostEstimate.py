from typing import Annotated, Optional, Literal, Union, Final
from pydantic import BaseModel, Field, field_validator
from Utils import Currency

TrafficCondition = Literal["light", "moderate", "heavy"]
TRAFFIC_CONDITION_WEIGHT: Final = {"light": 1.0, "moderate": 1.2, "heavy": 1.5}


class CostComponents(BaseModel):
    """The various components for calculating the total cost estimate for a **car** travel."""

    base_cost: Annotated[
        float, Field(default=5.0, gt=0, description="Fixed rate price")
    ]
    fuel_cost: Annotated[
        float, Field(default=10.0, gt=0, description="Cost of fuel based on distance")
    ]
    time_cost: Annotated[
        float, Field(default=0.5, gt=0, description="Cost associated with time spent")
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
    fuel_price: Annotated[
        Optional[float], Field(None, gt=0, description="Price of fuel")
    ]
    fuel_consumption: Annotated[
        Optional[float],
        Field(default=10, gt=0, description="Fuel consumption rate (e.g., km/l)"),
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

    @field_validator("traffic_adjustment", always=True)
    def validate_traffic_adjustment(cls, value):
        """Maps (if possible) and normalizes the traffic adjustment value based on its Weight."""

        if isinstance(value, str):
            return TRAFFIC_CONDITION_WEIGHT.get(value, 1.0)
        elif isinstance(value, (float, int)):
            return float(value)
        return 1.0


class CostEstimate(BaseModel):
    """Represents the estimated cost and its details associated with the cost calculation."""

    source_url: Annotated[
        Optional[str],
        Field(
            default="https://precos.petrobras.com.br/web/precos-dos-combustiveis/w/gasolina/",
            description="Endpoint source for the data used for the cost calculation.",
        ),
    ]
    source_description: str = Field(
        default="Official Petrobrás website. The data is collected via webscrapping."
    )
    estimated_cost: Annotated[float, Field(gt=0, description="Total estimated cost")]
    currency: Currency
    cost_details: CostComponents
