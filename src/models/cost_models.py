from typing import Annotated, Final, Literal, Union, get_args

from pydantic import BaseModel, Field, field_validator

from .utils_models import BaseQueryParams, Currency

TrafficCondition = Literal["light", "moderate", "heavy"]

TRAFFIC_CONDITION_WEIGHT: Final[dict[str, float]] = {
    "light": 1.0,
    "moderate": 1.2,
    "heavy": 1.5,
}


class CostEstimationParams(BaseQueryParams):
    state: Annotated[
        str, Field(..., description="The state for which to estimate the cost.", examples=["GO", "RS", "SP"])
    ]
    distance: Annotated[float, Field(..., gt=0, description="The distance of the travel in meters")]
    time_estimated: Annotated[int, Field(..., gt=0, description="The estimated time of travel in minutes")]
    # TODO: #8 Validate time assignment compatiblity across the app (seconds/minutes).
    traffic_condition: Annotated[
        TrafficCondition, Field(..., description="The traffic condition (light, moderate, heavy)")
    ]


class CostComponents(BaseModel):
    """The various components for calculating the total cost estimate for a car travel."""

    base_cost: Annotated[float, Field(default=0, ge=0, description="Fixed minimum rate price")]
    time_cost: Annotated[
        float,
        Field(
            default=0,
            ge=0,
            le=1.0,
            description="Cost associated with time spent",
        ),
    ]
    traffic_adjustment: Annotated[
        Union[TrafficCondition, float],
        Field(
            default=1.0,
            ge=1.0,
            le=1.5,
            description="Additional cost due to traffic conditions. It can be set as 'light', 'moderate' or 'heavy'",
        ),
    ]
    fuel_price: Annotated[float, Field(..., gt=0, description="Price of fuel")]
    fuel_consumption: Annotated[
        float,
        Field(
            default=0,
            ge=0,
            description="Fuel consumption rate (e.g. km/L)",
        ),
    ]

    # TODO: #9 Fix JSON schema validation error.
    # This causes the test_traffic_adjustment_valid_string_key to fail.

    # @field_validator("traffic_adjustment", mode="before")
    # @classmethod
    # def validate_traffic_adjustment(cls, value) -> float:
    #     """Maps and normalizes the traffic adjustment value based on its weight. Raises an error for unknown values."""
    #     if isinstance(value, str):
    #         if value not in get_args(TrafficCondition):
    #             raise ValueError(f"Unknown traffic condition '{value}'")
    #         return TRAFFIC_CONDITION_WEIGHT[value]
    #     elif isinstance(value, (float, int)):
    #         return float(value)
    #     raise ValueError(
    #         "Invalid type for traffic_adjustment. Must be one of: 'light', 'moderate', 'heavy' or a numeric value."
    #     )

    # @field_validator("traffic_adjustment", mode="before")
    # @classmethod
    # def validate_traffic_adjustment(cls, value) -> str:
    #     """Valida e converte o valor do ajuste de tráfego para o formato string correto."""
    #     # Se o valor for uma string, verificar se é válida
    #     if isinstance(value, str):
    #         if value not in get_args(TrafficCondition):
    #             raise ValueError(f"Unknown traffic condition '{value}'")
    #         return value

    #     # Se o valor for float, converter para a string correspondente
    #     elif isinstance(value, (float, int)):
    #         # Mapeando o peso para a condição de tráfego correta
    #         for condition, weight in TRAFFIC_CONDITION_WEIGHT.items():
    #             if weight == value:
    #                 return condition
    #         raise ValueError(f"Invalid traffic weight '{value}'")

    #     raise ValueError("Invalid type for traffic_adjustment. Must be one of: 'light', 'moderate', 'heavy' or a numeric value.")

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
        str,
        Field(
            default="",
            description="Endpoint source for the data used for the cost calculation.",
        ),
    ]
    source_description: str = Field(default="Official Petrobrás website. The data is collected via webscrapping.")
    estimated_cost: Annotated[float, Field(ge=0, description="Total estimated cost")]
    currency: Currency
    cost_details: CostComponents
