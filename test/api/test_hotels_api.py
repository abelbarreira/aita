import pytest
import requests
from aita.api import hotels_api


# fixture: ensure environment variables are set for all tests
@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch):
    monkeypatch.setenv("HOTEL_API_BASE_URL", "https://mockhotelapi.test")
    monkeypatch.setenv("HOTEL_API_KEY", "mockhotelkey123")


def test_search_hotels_success(mocker):
    # Prepare mock response
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "results": [{"hotel_id": "H123", "name": "Grand Hotel"}]
    }

    # Patch requests.get to return mock response
    mock_get = mocker.patch(
        "aita.api.hotels_api.requests.get", return_value=mock_response
    )

    query = {"city": "Paris"}
    results = hotels_api.search_hotels(query)

    # Assertions
    mock_get.assert_called_once()
    assert isinstance(results, list)
    assert results[0]["hotel_id"] == "H123"
    assert results[0]["name"] == "Grand Hotel"


def test_search_hotels_empty_response(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}

    mocker.patch("aita.api.hotels_api.requests.get", return_value=mock_response)

    results = hotels_api.search_hotels({"city": "Tokyo"})
    assert results == []


def test_search_hotels_api_failure(mocker):
    # Simulate API request exception (e.g. timeout, DNS error, etc.)
    mocker.patch(
        "aita.api.hotels_api.requests.get",
        side_effect=requests.RequestException("API is down"),
    )

    results = hotels_api.search_hotels({"city": "Berlin"})
    assert results == []


def test_search_hotels_env_not_set(monkeypatch):
    # Remove env vars to simulate missing configuration
    monkeypatch.delenv("HOTEL_API_BASE_URL", raising=False)
    monkeypatch.delenv("HOTEL_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="Hotel API base URL or API key not set"):
        hotels_api.search_hotels({"city": "Madrid"})
