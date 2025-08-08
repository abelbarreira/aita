import pytest
from aita.core import combo_engine


def test_search_travel_combinations(mocker):
    filters = {"destination": "Paris", "dates": "2025-12-20:2025-12-25"}

    # Mock build_flight_query and build_hotel_query
    mock_flight_query = {"from": "NYC", "to": "Paris", "dates": "2025-12-20:2025-12-25"}
    mock_hotel_query = {"location": "Paris", "dates": "2025-12-20:2025-12-25"}

    mocker.patch(
        "aita.core.combo_engine.build_flight_query", return_value=mock_flight_query
    )
    mocker.patch(
        "aita.core.combo_engine.build_hotel_query", return_value=mock_hotel_query
    )

    # Mock search_flights and search_hotels
    flight_results = [{"flight_id": "FL123", "price": 500}]
    hotel_results = [{"hotel_id": "HT456", "price_per_night": 150}]

    mocker.patch("aita.core.combo_engine.search_flights", return_value=flight_results)
    mocker.patch("aita.core.combo_engine.search_hotels", return_value=hotel_results)

    result = combo_engine.search_travel_combinations(filters)

    # Check if the queries were built correctly and search functions were called
    assert result == {"flights": flight_results, "hotels": hotel_results}

    # Optionally, assert that the mocks were called with expected parameters
    combo_engine.build_flight_query.assert_called_once_with(filters)
    combo_engine.build_hotel_query.assert_called_once_with(filters)
    combo_engine.search_flights.assert_called_once_with(mock_flight_query)
    combo_engine.search_hotels.assert_called_once_with(mock_hotel_query)
