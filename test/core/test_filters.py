import pytest
import os
import json
from typing import Any
from src.aita.core.filters import Filters, FlightFilters, HotelFilters


def load_test_vectors() -> list[dict[str, Any]]:
    """Loads test cases from the test_filters.json file."""
    current_dir: str = os.path.dirname(__file__)
    file_path: str = os.path.join(current_dir, "test_filters.json")
    with open(file_path, "r") as f:
        return json.load(f)


class TestFilters:
    """Class-based tests for Filters."""

    @classmethod
    def setup_class(cls) -> None:
        """Run once before all tests in this class."""
        pass

    @classmethod
    def teardown_class(cls) -> None:
        """Run once after all tests in this class."""
        pass

    def setup_method(self, method: Any) -> None:
        """Run before each test method."""
        pass

    def teardown_method(self, method: Any) -> None:
        """Run after each test method."""
        pass

    # Load vectors once at test collection (once per test session)
    @pytest.mark.parametrize("test_case", load_test_vectors())
    def test_from_prompt(self, test_case: dict[str, Any]) -> None:
        """Tests the from_prompt method of the Filters class."""
        prompt: str = test_case["prompt"]
        expected: dict[str, Any] = test_case["expected"]
        filter_instance: Filters = Filters.from_prompt(prompt)

        for key, expected_val in expected.items():
            if isinstance(expected_val, dict):
                actual_val: Any = getattr(filter_instance, key)
                assert isinstance(actual_val, dict) or hasattr(actual_val, "__dict__")
                for subkey, subval in expected_val.items():
                    actual_subval: Any = (
                        getattr(actual_val, subkey, None)
                        if hasattr(actual_val, "__dict__")
                        else actual_val.get(subkey)
                    )
                    assert (
                        actual_subval == subval
                    ), f"{key}.{subkey} mismatch: expected {subval}, got {actual_subval}"
            else:
                actual_val: Any = getattr(filter_instance, key, None)
                assert (
                    actual_val == expected_val
                ), f"{key} mismatch: expected {expected_val}, got {actual_val}"

    # Load vectors once at test collection (once per test session)
    @pytest.mark.parametrize("test_case", load_test_vectors())
    def test_check_missing_filters(self, test_case: dict[str, Any]) -> None:
        """Tests the check_missing_filters method of the Filters class."""
        prompt: str = test_case["prompt"]
        expected: dict[str, Any] = test_case["expected"]
        filter_instance: Filters = Filters.from_prompt(prompt)
        missing_attributes: list[str] = filter_instance.check_missing_filters()

        for key, expected_val in expected.items():
            if expected_val is None:
                assert key in missing_attributes, f"{key} should be reported as missing"
            elif isinstance(expected_val, dict):
                for subkey, subval in expected_val.items():
                    if subval is None:
                        assert (
                            f"{key}.{subkey}" in missing_attributes
                        ), f"{key}.{subkey} should be reported as missing"

    # Load vectors once at test collection (once per test session)
    @pytest.mark.parametrize("test_case", load_test_vectors())
    def test_matches(self, test_case: dict[str, Any]) -> None:
        """Tests the matches method of the Filters class."""
        prompt: str = test_case["prompt"]
        filter_instance_1: Filters = Filters.from_prompt(prompt)
        filter_instance_2: Filters = Filters.from_prompt(prompt)
        assert filter_instance_1.matches(filter_instance_2)

        if filter_instance_2.origin:
            filter_instance_2.origin = "ModifiedOrigin"
            assert not filter_instance_1.matches(filter_instance_2)

    def test_matches_none_attributes(self) -> None:
        f1: Filters = Filters(origin="A", destination=None)
        f2: Filters = Filters(origin="A", destination=None)
        assert f1.matches(f2) is True

        f3: Filters = Filters(origin="A", destination="B")
        f4: Filters = Filters(origin="A", destination=None)
        assert f3.matches(f4) is True

        f5: Filters = Filters(origin="A", destination="B")
        f6: Filters = Filters(origin="A", destination="C")
        assert f5.matches(f6) is False

    def test_check_missing_filters_nested(self) -> None:
        f: Filters = Filters()
        missing: list[str] = f.check_missing_filters()
        assert "origin" in missing
        assert "flight.departure_time_min" in missing
        assert "hotel.stars" in missing

    def test_pretty_print_covers_all(self, capsys: Any) -> None:
        f: Filters = Filters(
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
        out: str = capsys.readouterr().out
        assert "origin: A" in out
        assert "flight:" in out
        assert "hotel:" in out

    def test_matches_area_mismatch(self) -> None:
        f1: Filters = Filters(area="A")
        f2: Filters = Filters(area="B")
        assert f1.matches(f2) is False

    def test_matches_start_date_mismatch(self) -> None:
        f1: Filters = Filters(start_date="1 January")
        f2: Filters = Filters(start_date="2 January")
        assert f1.matches(f2) is False

    def test_matches_flight_departure_time_min_mismatch(self) -> None:
        f1: Filters = Filters(flight=FlightFilters(departure_time_min="08:00"))
        f2: Filters = Filters(flight=FlightFilters(departure_time_min="09:00"))
        assert f1.matches(f2) is False

    def test_matches_hotel_all_inclusive_mismatch(self) -> None:
        f1: Filters = Filters(hotel=HotelFilters(all_inclusive=True))
        f2: Filters = Filters(hotel=HotelFilters(all_inclusive=False))
        assert f1.matches(f2) is False

    def test_matches_hotel_distance_to_beach_greater(self) -> None:
        f1: Filters = Filters(hotel=HotelFilters(distance_to_beach=100))
        f2: Filters = Filters(hotel=HotelFilters(distance_to_beach=50))
        assert f1.matches(f2) is False
