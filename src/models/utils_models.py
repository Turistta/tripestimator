from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field

from config import settings


class BaseQueryParams(BaseModel):
    model_config = ConfigDict(extra="allow")

    api_key: str = settings.google_api_key  # type: ignore


class Currency(BaseModel):
    """Currency handler and parser"""

    model_config = ConfigDict(extra="forbid", strict=True)  # Enforce strict mode

    code: Annotated[
        Optional[str],  # Make fields Optional
        Field(
            default=None,  # Set default to None
            pattern=r"^[A-Z]{3}$",
            description="Currency code",
            examples=["BTC, USD"],
        ),
    ]
    symbol: Annotated[
        Optional[str],
        Field(
            default=None,
            min_length=1,
            max_length=10,
            description="Currency symbol",
            examples=["₿", "$"],
        ),
    ]
    name: Annotated[
        Optional[str],
        Field(
            default=None,
            min_length=2,
            max_length=30,
            description="Currency name",
            examples=["Bitcoin", "United States Dollar"],
        ),
    ]

    def __post_init__(self):
        any_attrs_provided = any(getattr(self, attr) is not None for attr in self.model_fields)

        if not any_attrs_provided:
            self.code = "BRL"
            self.symbol = "R$"
            self.name = "Brazilian Real"
