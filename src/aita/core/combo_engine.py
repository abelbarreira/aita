"""
Combo Engine: Coordinates flight and hotel searches based on user filters.
"""

from aita.api.flights_api import search_flights
from aita.api.hotels_api import search_hotels
from aita.core.query_builder import build_flight_query, build_hotel_query


def search_travel_combinations(filters: dict) -> dict:
    flight_query = build_flight_query(filters)
    hotel_query = build_hotel_query(filters)

    flight_results = search_flights(flight_query)
    hotel_results = search_hotels(hotel_query)

    return {"flights": flight_results, "hotels": hotel_results}
