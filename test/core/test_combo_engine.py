import pytest
from datetime import datetime
from aita.core.filters import Filters, FlightFilters, HotelFilters
from aita.core.query_dates import QueryDates
from aita.core import combo_engine


def test_search_travel_combinations(mocker):
    # Prepare Filters and QueryDates objects
    filters = Filters(
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
    query_dates = QueryDates(
        start_date=datetime(2025, 12, 20),
        end_date=datetime(2025, 12, 25),
    )

    # Mock QueryFlights and QueryHotels methods
    mock_flight_query = {"origin": "NYC", "destination": "Paris"}
    mock_hotel_query = {"destination": "Paris", "area": "Central"}

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
    flight_results = [{"flight_id": "FL123", "price": 500}]
    hotel_results = [{"hotel_id": "HT456", "price_per_night": 150}]

    mocker.patch("aita.core.combo_engine.search_flights", return_value=flight_results)
    mocker.patch("aita.core.combo_engine.search_hotels", return_value=hotel_results)

    result = combo_engine.search_travel_combinations(filters, query_dates)

    assert result == {"flights": flight_results, "hotels": hotel_results}

    # Optionally, assert that the mocks were called with expected parameters
    combo_engine.search_flights.assert_called_once_with(mock_flight_query)
    combo_engine.search_hotels.assert_called_once_with(mock_hotel_query)
