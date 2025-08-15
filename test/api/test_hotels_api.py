import pytest
import requests
from typing import Any
from aita.api import hotels_api


class TestHotelsApi:
    """Class-based tests for hotels_api."""

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

    @pytest.fixture(autouse=True)
    def _set_env_vars(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Ensure environment variables are set for all tests in this class."""
        monkeypatch.setenv("HOTEL_API_BASE_URL", "https://mockhotelapi.test")
        monkeypatch.setenv("HOTEL_API_KEY", "mockhotelkey123")

    def test_search_hotels_success(self, mocker: Any) -> None:
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{"hotel_id": "H123", "name": "Grand Hotel"}]
        }

        mock_get = mocker.patch(
            "aita.api.hotels_api.requests.get", return_value=mock_response
        )

        query: dict[str, str] = {"city": "Paris"}
        results: list = hotels_api.search_hotels(query)

        mock_get.assert_called_once()
        assert isinstance(results, list)
        assert results[0]["hotel_id"] == "H123"
        assert results[0]["name"] == "Grand Hotel"

    def test_search_hotels_empty_response(self, mocker: Any) -> None:
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}

        mocker.patch("aita.api.hotels_api.requests.get", return_value=mock_response)

        results: list = hotels_api.search_hotels({"city": "Tokyo"})
        assert results == []

    def test_search_hotels_api_failure(self, mocker: Any) -> None:
        mocker.patch(
            "aita.api.hotels_api.requests.get",
            side_effect=requests.RequestException("API is down"),
        )

        results: list = hotels_api.search_hotels({"city": "Berlin"})
        assert results == []

    def test_search_hotels_env_not_set(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("HOTEL_API_BASE_URL", raising=False)
        monkeypatch.delenv("HOTEL_API_KEY", raising=False)

        with pytest.raises(RuntimeError, match="Hotel API base URL or API key not set"):
            hotels_api.search_hotels({"city": "Madrid"})
