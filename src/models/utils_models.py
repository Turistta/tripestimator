from typing import Annotated
from pydantic import BaseModel, Field


class Currency(BaseModel):
    """Currency handler and parser"""

    code: Annotated[
        str,
        Field(
            default="BRL",
            regex=r"^[A-Z]{3}$",
            description="Currency code",
            examples=["BTC, USD"],
        ),
    ]
    symbol: Annotated[
        str,
        Field(
            default="R$",
            min_length=1,
            max_length=10,
            description="Currency symbol",
            examples=["₿", "$"],
        ),
    ]
    name: Annotated[
        str,
        Field(
            default="Brazilian Real",
            min_length=2,
            max_length=30,
            description="Currency name",
            examples=["Bitcoin", "United States Dollar"],
        ),
    ]
