"""
Combo Engine: Coordinates flight and hotel searches based on user filters.
"""

from aita.api.flights_api import search_flights
from aita.api.hotels_api import search_hotels
from aita.core.query_builder import QueryFlights, QueryHotels
from aita.core.filters import Filters
from aita.core.query_dates import QueryDates


def search_travel_combinations(filters: Filters, query_dates: QueryDates) -> dict:
    """
    Coordinates flight and hotel searches based on user filters and query dates.
    """
    flight_query = QueryFlights.from_filters(filters, query_dates).build_query_flights()
    hotel_query = QueryHotels.from_filters(filters, query_dates).build_query_hotels()

    flight_results = search_flights(flight_query)
    hotel_results = search_hotels(hotel_query)

    return {"flights": flight_results, "hotels": hotel_results}
