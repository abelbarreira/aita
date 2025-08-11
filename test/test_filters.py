import pytest
import json
from src.aita.core.filters import Filters, FlightFilters, HotelFilters


def load_test_cases():
    """
    Loads test cases from the test_filters.json file.
    """
    with open("test/test_filters.json", "r") as f:
        return json.load(f)


@pytest.mark.parametrize("test_case", load_test_cases())
def test_from_prompt(test_case):
    """
    Tests the from_prompt method of the Filters class.
    """
    prompt = test_case["prompt"]
    expected = test_case["expected"]

    # Create a Filters instance from the prompt
    filter_instance = Filters.from_prompt(prompt)

    # Validate the attributes of the Filters instance
    for key, expected_val in expected.items():
        if isinstance(expected_val, dict):
            # Handle nested attributes (e.g., hotel, flight)
            actual_val = getattr(filter_instance, key)
            assert isinstance(actual_val, dict) or hasattr(
                actual_val, "__dict__"
            ), f"{key} should be a dict or object"
            for subkey, subval in expected_val.items():
                actual_subval = (
                    getattr(actual_val, subkey, None)
                    if hasattr(actual_val, "__dict__")
                    else actual_val.get(subkey)
                )
                assert (
                    actual_subval == subval
                ), f"{key}.{subkey} mismatch: expected {subval}, got {actual_subval}"
        else:
            # Handle top-level attributes
            actual_val = getattr(filter_instance, key, None)
            assert (
                actual_val == expected_val
            ), f"{key} mismatch: expected {expected_val}, got {actual_val}"


@pytest.mark.parametrize("test_case", load_test_cases())
def test_check_missing_filters(test_case):
    """
    Tests the check_missing_filters method of the Filters class.
    """
    prompt = test_case["prompt"]
    expected = test_case["expected"]

    # Create a Filters instance from the prompt
    filter_instance = Filters.from_prompt(prompt)

    # Check for missing attributes
    missing_attributes = filter_instance.check_missing_filters()

    # Ensure that attributes explicitly set to None in the expected result are reported as missing
    for key, expected_val in expected.items():
        if expected_val is None:
            assert key in missing_attributes, f"{key} should be reported as missing"
        elif isinstance(expected_val, dict):
            for subkey, subval in expected_val.items():
                if subval is None:
                    assert (
                        f"{key}.{subkey}" in missing_attributes
                    ), f"{key}.{subkey} should be reported as missing"


@pytest.mark.parametrize("test_case", load_test_cases())
def test_matches(test_case):
    """
    Tests the matches method of the Filters class.
    """
    prompt = test_case["prompt"]

    # Create two Filters instances from the same prompt
    filter_instance_1 = Filters.from_prompt(prompt)
    filter_instance_2 = Filters.from_prompt(prompt)

    # Ensure that the two instances match
    assert filter_instance_1.matches(
        filter_instance_2
    ), "Filters instances should match"

    # Modify one of the attributes in the second instance to ensure it no longer matches
    if filter_instance_2.origin:
        filter_instance_2.origin = "ModifiedOrigin"
        assert not filter_instance_1.matches(
            filter_instance_2
        ), "Filters instances should not match after modification"


def test_matches_none_attributes():
    # Only origin is set, rest are None
    f1 = Filters(origin="A", destination=None)
    f2 = Filters(origin="A", destination=None)
    assert f1.matches(f2) is True

    # One has None, one has value
    f3 = Filters(origin="A", destination="B")
    f4 = Filters(origin="A", destination=None)
    assert f3.matches(f4) is True  # destination is ignored if one is None

    # Both set, but different
    f5 = Filters(origin="A", destination="B")
    f6 = Filters(origin="A", destination="C")
    assert f5.matches(f6) is False


def test_check_missing_filters_nested():
    f = Filters()
    missing = f.check_missing_filters()
    assert "origin" in missing
    assert "flight.departure_time_min" in missing
    assert "hotel.stars" in missing


def test_pretty_print_covers_all(capsys):
    f = Filters(
        origin="A",
        destination="B",
        area="C",
        start_date="1 January",
        duration_min=1,
        duration_max=2,
        flexibility=1,
        flight=FlightFilters(
            departure_time_min="08:00", departure_time_max="10:00", direct=True
        ),
        hotel=HotelFilters(stars=5, all_inclusive=True, distance_to_beach=100.0),
    )
    f.pretty_print()
    out = capsys.readouterr().out
    assert "origin: A" in out
    assert "flight:" in out
    assert "hotel:" in out


def test_matches_area_mismatch():
    f1 = Filters(area="A")
    f2 = Filters(area="B")
    assert f1.matches(f2) is False  # covers line 149


def test_matches_start_date_mismatch():
    f1 = Filters(start_date="1 January")
    f2 = Filters(start_date="2 January")
    assert f1.matches(f2) is False  # covers line 151


def test_matches_flight_departure_time_min_mismatch():
    f1 = Filters(flight=FlightFilters(departure_time_min="08:00"))
    f2 = Filters(flight=FlightFilters(departure_time_min="09:00"))
    assert f1.matches(f2) is False  # covers line 173


def test_matches_hotel_all_inclusive_mismatch():
    f1 = Filters(hotel=HotelFilters(all_inclusive=True))
    f2 = Filters(hotel=HotelFilters(all_inclusive=False))
    # Both are not None, so this will trigger the mismatch
    assert f1.matches(f2) is False


def test_matches_hotel_distance_to_beach_greater():
    f1 = Filters(hotel=HotelFilters(distance_to_beach=100))
    f2 = Filters(hotel=HotelFilters(distance_to_beach=50))
    # Both are not None, and 100 > 50, so this will trigger the mismatch
    assert f1.matches(f2) is False


def test_matches_hotel_all_inclusive_mismatch():
    f1 = Filters(hotel=HotelFilters(all_inclusive=True))
    f2 = Filters(hotel=HotelFilters(all_inclusive=False))
    # Both are not None, so this will trigger the mismatch
    assert f1.matches(f2) is False
