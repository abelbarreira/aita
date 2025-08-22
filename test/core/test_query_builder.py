from datetime import datetime
from typing import Any

import pytest

from aita.core.filters import Filters, FlightFilters, HotelFilters
from aita.core.query_builder import QueryFlights, QueryHotels
from aita.core.query_dates import QueryDates


@pytest.fixture(scope="module")
def filters_obj() -> Filters:
    """Module-level Filters fixture."""
    return Filters(
        origin="Copenhagen",
        destination="Tokyo",
        area="Shibuya",
        start_date="5 September",
        duration_min=5,
        duration_max=10,
        flexibility=1,
        flight=FlightFilters(
            departure_time_min="08:00",
            departure_time_max="12:00",
            direct=True,
        ),
        hotel=HotelFilters(
            stars=4,
            all_inclusive=True,
            distance_to_beach=500.0,
        ),
    )


@pytest.fixture(scope="module")
def query_dates_obj() -> QueryDates:
    """Module-level QueryDates fixture."""
    return QueryDates(
        start_date=datetime(2025, 9, 5),
        end_date=datetime(2025, 9, 15),
    )


class TestQueryBuilder:
    """Class-based tests for QueryFlights and QueryHotels."""

    @classmethod
    def setup_class(cls) -> None:
        """Run once before all tests in this class."""
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

    def test_query_flights_from_filters(
        self, filters_obj: Filters, query_dates_obj: QueryDates
    ) -> None:
        qf: QueryFlights = QueryFlights.from_filters(filters_obj, query_dates_obj)
        assert qf.origin == "Copenhagen"
        assert qf.destination == "Tokyo"
        assert qf.flight.departure_time_min == "08:00"
        assert qf.query_dates == query_dates_obj

    def test_query_flights_build_query(
        self, filters_obj: Filters, query_dates_obj: QueryDates
    ) -> None:
        qf: QueryFlights = QueryFlights.from_filters(filters_obj, query_dates_obj)
        query: dict = qf.build_query_flights()
        assert query == {
            "origin": "Copenhagen",
            "destination": "Tokyo",
            "start_date": "2025-09-05",
            "end_date": "2025-09-15",
            "departure_time_min": "08:00",
            "departure_time_max": "12:00",
            "direct": True,
        }

    def test_query_hotels_from_filters(
        self, filters_obj: Filters, query_dates_obj: QueryDates
    ) -> None:
        qh: QueryHotels = QueryHotels.from_filters(filters_obj, query_dates_obj)
        assert qh.destination == "Tokyo"
        assert qh.area == "Shibuya"
        assert qh.hotel.stars == 4
        assert qh.query_dates == query_dates_obj

    def test_query_hotels_build_query(
        self, filters_obj: Filters, query_dates_obj: QueryDates
    ) -> None:
        qh: QueryHotels = QueryHotels.from_filters(filters_obj, query_dates_obj)
        query: dict = qh.build_query_hotels()
        assert query == {
            "destination": "Tokyo",
            "area": "Shibuya",
            "start_date": "2025-09-05",
            "end_date": "2025-09-15",
            "stars": 4,
            "all_inclusive": True,
            "distance_to_beach": 500.0,
        }

    def test_query_flights_defaults(self, query_dates_obj: QueryDates) -> None:
        qf: QueryFlights = QueryFlights(query_dates=query_dates_obj)
        query: dict = qf.build_query_flights()
        assert query["origin"] is None
        assert query["departure_time_min"] is None
        assert query["direct"] is None

    def test_query_hotels_defaults(self, query_dates_obj: QueryDates) -> None:
        qh: QueryHotels = QueryHotels(query_dates=query_dates_obj)
        query: dict = qh.build_query_hotels()
        assert query["destination"] is None
        assert query["stars"] is None
        assert query["all_inclusive"] is None
