from app.aita.core.query_builder import build_flight_query, build_hotel_query


def test_build_flight_query():
    filters = {
        "origin": "Copenhagen",
        "destination": "Palma de Mallorca",
        "month": "September",
        "duration": {"min": 7, "max": 10},
        "flight": {"departure_time": {"from": "08:00", "to": "19:00"}},
        "currency": "EUR",
    }
    query = build_flight_query(filters)
    assert query["origin"] == "Copenhagen"
    assert query["duration_min"] == 7


def test_build_hotel_query():
    filters = {
        "destination": "Palma de Mallorca",
        "area": "Playa Magaluf",
        "hotel": {
            "proximity_to_beach": "300 meters",
            "stars": 4,
            "board": "All-Inclusive",
        },
    }
    query = build_hotel_query(filters)
    assert query["area"] == "Playa Magaluf"
    assert query["stars"] == 4
