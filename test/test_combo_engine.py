from unittest.mock import patch
from aita.core.combo_engine import search_travel_combinations


@patch("aita.core.combo_engine.search_hotels")
@patch("aita.core.combo_engine.search_flights")
def test_search_travel_combinations(mock_flights, mock_hotels):
    mock_flights.return_value = [{"flight_id": "F1"}]
    mock_hotels.return_value = [{"hotel_id": "H1"}]

    filters = {
        "origin": "Copenhagen",
        "destination": "Rome",
        "month": "July",
        "duration": {"min": 5, "max": 10},
        "flight": {"departure_time": {"from": "08:00", "to": "12:00"}},
        "hotel": {
            "stars": 4,
            "board": "All-Inclusive",
        },
    }

    result = search_travel_combinations(filters)

    mock_flights.assert_called_once()
    mock_hotels.assert_called_once()

    assert result["flights"] == [{"flight_id": "F1"}]
    assert result["hotels"] == [{"hotel_id": "H1"}]
