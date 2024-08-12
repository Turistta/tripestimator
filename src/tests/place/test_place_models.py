import pytest

from models.place_models import (
    FindPlaceQueryParams,
    NearbySearchQueryParams,
    QueryParamsFactory,
    TextSearchQueryParams,
)


def test_empty_params() -> None:
    with pytest.raises(ValueError, match="Invalid parameters: Empty query"):
        QueryParamsFactory({})


@pytest.mark.parametrize(
    "params, expected_class",
    [
        ({"location": {"latitude": 40.7128, "longitude": -74.0060}, "radius": 1000}, NearbySearchQueryParams),
        ({"text_input": "Morrinhos", "inputtype": "textquery"}, FindPlaceQueryParams),
        ({"query": "churrasco", "radius": 1200}, TextSearchQueryParams),
    ],
)
def test_different_param_combinations(params, expected_class) -> None:
    factory = QueryParamsFactory(params)
    assert isinstance(factory.query_params_class, type(expected_class))
    model = factory.create_query_model()
    assert isinstance(model, expected_class)
