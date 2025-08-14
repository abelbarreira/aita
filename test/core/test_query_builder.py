import pytest
from datetime import datetime
from aita.core.filters import Filters, FlightFilters, HotelFilters
from aita.core.query_dates import QueryDates
from aita.core.query_builder import QueryFlights, QueryHotels


@pytest.fixture
def filters_obj():
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


@pytest.fixture
def query_dates_obj():
    return QueryDates(
        start_date=datetime(2025, 9, 5),
        end_date=datetime(2025, 9, 15),
    )


def test_query_flights_from_filters(filters_obj, query_dates_obj):
    qf = QueryFlights.from_filters(filters_obj, query_dates_obj)
    assert qf.origin == "Copenhagen"
    assert qf.destination == "Tokyo"
    assert qf.flight.departure_time_min == "08:00"
    assert qf.query_dates == query_dates_obj


def test_query_flights_build_query(filters_obj, query_dates_obj):
    qf = QueryFlights.from_filters(filters_obj, query_dates_obj)
    query = qf.build_query_flights()
    assert query == {
        "origin": "Copenhagen",
        "destination": "Tokyo",
        "start_date": "2025-09-05",
        "end_date": "2025-09-15",
        "departure_time_min": "08:00",
        "departure_time_max": "12:00",
        "direct": True,
    }


def test_query_hotels_from_filters(filters_obj, query_dates_obj):
    qh = QueryHotels.from_filters(filters_obj, query_dates_obj)
    assert qh.destination == "Tokyo"
    assert qh.area == "Shibuya"
    assert qh.hotel.stars == 4
    assert qh.query_dates == query_dates_obj


def test_query_hotels_build_query(filters_obj, query_dates_obj):
    qh = QueryHotels.from_filters(filters_obj, query_dates_obj)
    query = qh.build_query_hotels()
    assert query == {
        "destination": "Tokyo",
        "area": "Shibuya",
        "start_date": "2025-09-05",
        "end_date": "2025-09-15",
        "stars": 4,
        "all_inclusive": True,
        "distance_to_beach": 500.0,
    }


def test_query_flights_defaults(query_dates_obj):
    qf = QueryFlights(query_dates=query_dates_obj)
    query = qf.build_query_flights()
    assert query["origin"] is None
    assert query["departure_time_min"] is None
    assert query["direct"] is None


def test_query_hotels_defaults(query_dates_obj):
    qh = QueryHotels(query_dates=query_dates_obj)
    query = qh.build_query_hotels()
    assert query["destination"] is None
    assert query["stars"] is None
    assert query["all_inclusive"] is None
