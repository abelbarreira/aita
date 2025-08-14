import pytest
import os
from aita.api import flights_api_priceline_com2
from aita.core.query_dates import generate_query_dates
from aita.core.filters import Filters, FlightFilters, HotelFilters
from aita.core.query_builder import QueryFlights

try:
    from dotenv import load_dotenv
except ImportError:
    print("Missing 'python-dotenv'. Please install with: pip install python-dotenv")
    exit(1)

REQUIRED_KEYS = [
    "CURRENCY",
    "FLIGHT_API_BASE_URL",
    "FLIGHT_API_KEY",
    "HOTEL_API_BASE_URL",
    "HOTEL_API_KEY",
]


def check_env_keys(required_keys):
    missing = []
    for key in required_keys:
        if not os.getenv(key):
            missing.append(key)
    return missing


@pytest.fixture
def filters_obj():
    return Filters(
        origin="Copenhagen",
        destination="Mallorca",
        area="Magaluf",
        start_date="5 September",
        duration_min=5,
        duration_max=6,
        flexibility=1,
        flight=FlightFilters(
            departure_time_min="08:00",
            departure_time_max="19:00",
            direct=True,
        ),
        hotel=HotelFilters(
            stars=4,
            all_inclusive=True,
            distance_to_beach=500.0,
        ),
    )


def test_search_flights_success(filters_obj):
    load_dotenv()
    missing_keys = check_env_keys(REQUIRED_KEYS)
    if missing_keys:
        pytest.skip(f"Missing keys in .env file: {missing_keys}")

    query_dates_dic_obj = generate_query_dates(filters_obj)
    query_flights = QueryFlights.from_filters(filters_obj, query_dates_dic_obj[0])
    query_flights.pretty_print()

    results = flights_api_priceline_com2.search_flights(query_flights)

    assert results is not None
    assert isinstance(results, dict)
    # Optionally, check for expected keys in results
