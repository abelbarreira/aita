"""
Query Builder: Converts structured filters into API query parameters.
"""


def build_flight_query(filters: dict) -> dict:
    return {
        "origin": filters.get("origin"),
        "destination": filters.get("destination"),
        "month": filters.get("month"),
        "duration_min": filters["duration"]["min"],
        "duration_max": filters["duration"]["max"],
        "departure_time_from": filters["flight"].get("departure_time", {}).get("from"),
        "departure_time_to": filters["flight"].get("departure_time", {}).get("to"),
        "currency": filters.get("currency"),
    }


def build_hotel_query(filters: dict) -> dict:
    return {
        "destination": filters.get("destination"),
        "area": filters.get("area"),
        "proximity_to_beach": filters["hotel"].get("proximity_to_beach"),
        "stars": filters["hotel"].get("stars"),
        "board": filters["hotel"].get("board"),
    }
