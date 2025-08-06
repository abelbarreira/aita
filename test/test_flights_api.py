import os
import pytest
from unittest.mock import patch
from aita.api import flights_api


@patch.dict(
    os.environ,
    {"FLIGHT_API_BASE_URL": "https://mockapi.test", "FLIGHT_API_KEY": "mockkey123"},
)
@patch("aita.api.flights_api.requests.get")
def test_search_flights_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "results": [{"flight_id": "123", "price": 200}]
    }

    query = {"origin": "Copenhagen", "destination": "Rome"}
    results = flights_api.search_flights(query)

    mock_get.assert_called_once()
    assert isinstance(results, list)
    assert results[0]["flight_id"] == "123"


@patch.dict(
    os.environ,
    {"FLIGHT_API_BASE_URL": "https://mockapi.test", "FLIGHT_API_KEY": "mockkey123"},
)
@patch("aita.api.flights_api.requests.get")
def test_search_flights_failure(mock_get):
    mock_get.side_effect = Exception("API down")

    with pytest.raises(Exception) as exc_info:
        flights_api.search_flights({"origin": "Copenhagen"})

    assert str(exc_info.value) == "API down"
