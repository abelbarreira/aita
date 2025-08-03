import pytest
from app.core.prompt_parser import parse_prompt

def test_parse_prompt_basic():
    prompt = 'Find me Flights and Hotels from "Copenhagen" to "Palma de Mallorca", area "Playa Magaluf", in "September", staying between "7" to "10" days. Hotels: Within "300 meters" from the beach, "4" stars, "All-Inclusive". Flights: Departing between "08:00" and "19:00".'
    result = parse_prompt(prompt)
    assert result["origin"] == "Copenhagen"
    assert result["destination"] == "Palma de Mallorca"
    assert result["area"] == "Playa Magaluf"
    assert result["month"] == "September"
    assert result["duration"]["min"] == 7
    assert result["duration"]["max"] == 10
    assert result["hotel"]["stars"] == 4
    assert result["hotel"]["board"] == "All-Inclusive"
    assert result["flight"]["departure_time"]["from"] == "08:00"
