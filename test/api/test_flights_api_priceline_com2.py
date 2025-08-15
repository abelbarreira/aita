import pytest
from aita.api import flights_api_priceline_com2
from aita.core.query_dates import generate_query_dates, pretty_print_query_dates
from aita.core.filters import Filters, FlightFilters, HotelFilters
from aita.core.query_builder import QueryFlights
from aita.core.results_builder import (
    Result,
    pretty_print_result,
)


@pytest.fixture
def filters_obj():
    return Filters(
        origin="Copenhagen",
        destination="Mallorca",
        area="Magaluf",
        start_date="22 September",
        duration_min=5,
        duration_max=5,
        flexibility=1,
        flight=FlightFilters(
            departure_time_min="00:01",
            departure_time_max="23:59",
            direct=True,
        ),
        hotel=HotelFilters(
            stars=4,
            all_inclusive=True,
            distance_to_beach=500.0,
        ),
    )


def test_search_flights_success(filters_obj):
    query_dates = generate_query_dates(filters_obj)

    # print("\nDates:", len(query_dates))
    # pretty_print_query_dates(query_dates)

    print("\nSearching flights with the following parameters...")

    for idx, query_date in query_dates.items():

        query_flights = QueryFlights.from_filters(filters_obj, query_date)
        results: dict[int, Result] = flights_api_priceline_com2.search_flights(
            query_flights
        )

        print(
            f"\n\n\nStart = {query_dates[idx].start_date.strftime('%Y-%m-%d')}\nEnd   = {query_dates[idx].end_date.strftime('%Y-%m-%d')}\n"
        )
        pretty_print_result(results)

        assert results is not None
        assert isinstance(results, dict)
        # Optionally, check for expected keys in result_flights

    print("\nDone searching flights!\n")
