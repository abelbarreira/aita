from datetime import datetime
from typing import Any

from aita.core import combo_engine
from aita.core.filters import Filters, FlightFilters, HotelFilters
from aita.core.query_dates import QueryDates


class TestComboEngine:
    """Class-based tests for combo_engine."""

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

    def test_search_travel_combinations(self, mocker: Any) -> None:
        # Prepare Filters and QueryDates objects
        filters: Filters = Filters(
            origin="NYC",
            destination="Paris",
            area="Central",
            start_date="20 December",
            duration_min=5,
            duration_max=5,
            flexibility=0,
            flight=FlightFilters(
                departure_time_min="09:00",
                departure_time_max="18:00",
                direct=True,
            ),
            hotel=HotelFilters(
                stars=4,
                all_inclusive=True,
                distance_to_beach=200.0,
            ),
        )
        query_dates: QueryDates = QueryDates(
            start_date=datetime(2025, 12, 20),
            end_date=datetime(2025, 12, 25),
        )

        # Mock QueryFlights and QueryHotels methods
        mock_flight_query: dict[str, str] = {"origin": "NYC", "destination": "Paris"}
        mock_hotel_query: dict[str, str] = {"destination": "Paris", "area": "Central"}

        mocker.patch(
            "aita.core.query_builder.QueryFlights.from_filters",
            return_value=mocker.Mock(
                build_query_flights=mocker.Mock(return_value=mock_flight_query)
            ),
        )
        mocker.patch(
            "aita.core.query_builder.QueryHotels.from_filters",
            return_value=mocker.Mock(
                build_query_hotels=mocker.Mock(return_value=mock_hotel_query)
            ),
        )

        # Mock search_flights and search_hotels
        flight_results: list[dict[str, Any]] = [{"flight_id": "FL123", "price": 500}]
        hotel_results: list[dict[str, Any]] = [
            {"hotel_id": "HT456", "price_per_night": 150}
        ]

        mock_search_flights = mocker.patch(
            "aita.core.combo_engine.search_flights", return_value=flight_results
        )
        mock_search_hotels = mocker.patch(
            "aita.core.combo_engine.search_hotels", return_value=hotel_results
        )

        result: dict[str, list[dict[str, Any]]] = combo_engine.search_travel_combinations(
            filters, query_dates
        )

        assert result == {"flights": flight_results, "hotels": hotel_results}

        # Assert that the mocks were called with expected parameters
        mock_search_flights.assert_called_once_with(mock_flight_query)
        mock_search_hotels.assert_called_once_with(mock_hotel_query)
