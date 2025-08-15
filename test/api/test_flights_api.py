import pytest
import requests
from typing import Any
from aita.api import flights_api


class TestFlightsApi:
    @classmethod
    def setup_class(cls) -> None:
        """Run once before any tests in this class."""
        pass

    @classmethod
    def teardown_class(cls) -> None:
        """Run once after all tests in this class."""
        pass

    def setup_method(self, method: Any) -> None:
        """Run before each test method."""
        pass

    def teardown_method(self, method: Any) -> None:
        """Run after each test method."""
        pass

    @pytest.fixture(autouse=True)  # runs before every test method in this class only
    def _set_env_vars(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Ensure environment variables are set before each test using monkeypatch fixture."""
        monkeypatch.setenv("FLIGHT_API_BASE_URL", "https://mockapi.test")
        monkeypatch.setenv("FLIGHT_API_KEY", "mockkey123")

    def test_search_flights_success(self, mocker: Any) -> None:
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{"flight_id": "123", "price": 200}]
        }

        mock_get = mocker.patch(
            "aita.api.flights_api.requests.get", return_value=mock_response
        )

        query: dict[str, str] = {"origin": "Copenhagen", "destination": "Rome"}
        results: list = flights_api.search_flights(query)

        mock_get.assert_called_once_with(
            "https://mockapi.test/search",
            params=query,
            headers={"Authorization": "Bearer mockkey123"},
        )

        assert isinstance(results, list)
        assert results[0]["flight_id"] == "123"
        assert results[0]["price"] == 200

    def test_search_flights_empty_response(self, mocker: Any) -> None:
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}

        mocker.patch("aita.api.flights_api.requests.get", return_value=mock_response)

        results: list = flights_api.search_flights({"origin": "Oslo"})
        assert results == []

    def test_search_flights_failure(self, mocker: Any) -> None:
        mocker.patch(
            "aita.api.flights_api.requests.get",
            side_effect=requests.RequestException("API is down"),
        )

        results: list = flights_api.search_flights({"origin": "Berlin"})
        assert results == []

    def test_search_hotels_env_not_set(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Remove env vars to simulate missing configuration
        monkeypatch.delenv("FLIGHT_API_BASE_URL", raising=False)
        monkeypatch.delenv("FLIGHT_API_KEY", raising=False)

        with pytest.raises(
            RuntimeError, match="Flight API base URL or API key not set"
        ):
            query: dict[str, str] = {"origin": "Copenhagen", "destination": "Rome"}
            flights_api.search_flights(query)
