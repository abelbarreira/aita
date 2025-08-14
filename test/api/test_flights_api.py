import pytest
import requests
from aita.api import flights_api


# fixture: ensure environment variables are set for all tests
@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch):
    # monkeypatch.setenv(...): modify os.environ for the duration of the test
    #                          after test run, pytest will automatically restore it
    monkeypatch.setenv("FLIGHT_API_BASE_URL", "https://mockapi.test")
    monkeypatch.setenv("FLIGHT_API_KEY", "mockkey123")


def test_search_flights_success(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"results": [{"flight_id": "123", "price": 200}]}

    mock_get = mocker.patch(
        "aita.api.flights_api.requests.get", return_value=mock_response
    )

    query = {"origin": "Copenhagen", "destination": "Rome"}
    results = flights_api.search_flights(query)

    mock_get.assert_called_once_with(  # check requests.get was called exactly once
        "https://mockapi.test/search",
        params=query,
        headers={"Authorization": "Bearer mockkey123"},
    )

    assert isinstance(results, list)
    assert results[0]["flight_id"] == "123"
    assert results[0]["price"] == 200


def test_search_flights_empty_response(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}

    mocker.patch("aita.api.flights_api.requests.get", return_value=mock_response)

    results = flights_api.search_flights({"origin": "Oslo"})
    assert results == []


def test_search_flights_failure(mocker):
    # Mock requests.get to raise a *RequestException*, which your code is designed to catch
    mocker.patch(
        "aita.api.flights_api.requests.get",
        side_effect=requests.RequestException("API is down"),
    )

    # Call the function
    results = flights_api.search_flights({"origin": "Berlin"})

    # Should return empty list due to exception handling
    assert results == []


def test_search_hotels_env_not_set(monkeypatch):
    # Remove env vars to simulate missing configuration
    monkeypatch.delenv("FLIGHT_API_BASE_URL", raising=False)
    monkeypatch.delenv("FLIGHT_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="Flight API base URL or API key not set"):
        query = {"origin": "Copenhagen", "destination": "Rome"}
        flights_api.search_flights(query)
