import pytest
from aita.core.query_builder import build_flight_query, build_hotel_query


@pytest.fixture
def full_filters():
    return {
        "origin": "Copenhagen",
        "destination": "Tokyo",
        "month": "September",
        "duration": {"min": 5, "max": 10},
        "flight": {"departure_time": {"from": "08:00", "to": "12:00"}},
        "hotel": {"proximity_to_beach": "500m", "stars": 4, "board": "All-Inclusive"},
        "area": "Shibuya",
        "currency": "EUR",
    }


def test_build_flight_query(full_filters):
    query = build_flight_query(full_filters)
    assert query == {
        "origin": "Copenhagen",
        "destination": "Tokyo",
        "month": "September",
        "duration_min": 5,
        "duration_max": 10,
        "departure_time_from": "08:00",
        "departure_time_to": "12:00",
        "currency": "EUR",
    }


def test_build_hotel_query(full_filters):
    query = build_hotel_query(full_filters)
    assert query == {
        "destination": "Tokyo",
        "area": "Shibuya",
        "proximity_to_beach": "500m",
        "stars": 4,
        "board": "All-Inclusive",
    }


def test_missing_optional_fields():
    minimal_filters = {
        "origin": "Paris",
        "destination": "Rome",
        "duration": {"min": None, "max": None},
        "flight": {},
        "hotel": {},
    }

    flight_query = build_flight_query(minimal_filters)
    assert flight_query["origin"] == "Paris"
    assert flight_query["departure_time_from"] is None

    hotel_query = build_hotel_query(minimal_filters)
    assert hotel_query["stars"] is None
    assert hotel_query["board"] is None
