import os
import pytest
from unittest.mock import patch
from aita.api import hotels_api


@patch.dict(
    os.environ,
    {"HOTEL_API_BASE_URL": "https://mockapi.test", "HOTEL_API_KEY": "mockkey123"},
)
@patch("aita.api.hotels_api.requests.get")
def test_search_hotels_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "results": [{"hotel_id": "h1", "name": "Beach Resort"}]
    }

    query = {"destination": "Rome", "stars": 4}
    results = hotels_api.search_hotels(query)

    mock_get.assert_called_once()
    assert isinstance(results, list)
    assert results[0]["name"] == "Beach Resort"


import pytest
import os
from unittest.mock import patch
from aita.api import hotels_api


@patch.dict(
    os.environ,
    {"HOTEL_API_BASE_URL": "https://mockapi.test", "HOTEL_API_KEY": "mockkey123"},
)
@patch("aita.api.hotels_api.requests.get")
def test_search_hotels_failure(mock_get):
    mock_get.side_effect = Exception("API not responding")

    with pytest.raises(Exception) as exc_info:
        hotels_api.search_hotels({"destination": "Rome"})

    assert str(exc_info.value) == "API not responding"
