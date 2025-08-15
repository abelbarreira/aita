import pytest
import os
import json
from datetime import datetime
from typing import Any
from aita.core.query_dates import (
    generate_query_dates,
    QueryDates,
    pretty_print_query_dates,
)
from aita.core.filters import Filters


def load_test_vectors() -> list[dict[str, Any]]:
    """Load test vectors from JSON file located in the same folder as the test."""
    current_dir: str = os.path.dirname(__file__)
    file_path: str = os.path.join(current_dir, "test_query_dates.json")
    with open(file_path, "r") as f:
        test_vectors = json.load(f)

    # Convert filter_obj dicts into Filters objects
    for vector in test_vectors:
        vector["filter_obj"] = Filters(**vector["filter_obj"])
    return test_vectors


class TestQueryDates:
    """Class-based tests for generate_query_dates and related utilities."""

    @classmethod
    def setup_class(cls) -> None:
        """Run once before all tests in this class."""
        cls.test_vectors = load_test_vectors()

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
    @pytest.mark.parametrize("test_vector", load_test_vectors())
    def test_generate_query_dates(self, test_vector: dict[str, Any]) -> None:
        """Test generate_query_dates using test vectors."""
        filter_obj = test_vector["filter_obj"]
        expected_combinations = test_vector["expected_combinations"]
        first_query = test_vector["first_query"]
        last_query = test_vector["last_query"]

        # Generate query dates
        query_dates = generate_query_dates(filter_obj)

        # Validate number of combinations
        assert (
            len(query_dates) == expected_combinations
        ), "Incorrect number of QueryDates generated"

        # Validate first QueryDates
        first_generated = query_dates[0]
        assert first_generated.start_date == datetime.strptime(
            first_query["start_date"], "%d %B %Y"
        )
        assert first_generated.end_date == datetime.strptime(
            first_query["end_date"], "%d %B %Y"
        )

        # Validate last QueryDates
        last_index = max(query_dates.keys())
        last_generated = query_dates[last_index]
        assert last_generated.start_date == datetime.strptime(
            last_query["start_date"], "%d %B %Y"
        )
        assert last_generated.end_date == datetime.strptime(
            last_query["end_date"], "%d %B %Y"
        )

    def test_generate_query_dates_missing_parameters(self) -> None:
        """Test that generate_query_dates raises ValueError for missing parameters."""
        filter_obj = Filters(
            start_date=None, flexibility=2, duration_min=3, duration_max=5
        )
        with pytest.raises(
            ValueError,
            match="Filters object must have start_date, flexibility, duration_min, and duration_max defined.",
        ):
            generate_query_dates(filter_obj)

    def test_generate_query_dates_edge_case(self) -> None:
        """Test generate_query_dates with edge case values."""
        filter_obj = Filters(
            start_date="15 December", flexibility=0, duration_min=5, duration_max=5
        )
        query_dates = generate_query_dates(filter_obj)

        # Only one combination expected
        assert (
            len(query_dates) == 1
        ), "Incorrect number of QueryDates generated for edge case"

        single_query = query_dates[0]
        assert single_query.start_date == datetime.strptime(
            "15 December 2025", "%d %B %Y"
        )
        assert single_query.end_date == datetime.strptime(
            "20 December 2025", "%d %B %Y"
        )

    def test_pretty_print_query_dates(self, capsys: Any) -> None:
        """Test pretty_print_query_dates prints the expected output."""
        query_dates_dict = {
            0: QueryDates(
                start_date=datetime(2025, 1, 5), end_date=datetime(2025, 1, 12)
            ),
            1: QueryDates(
                start_date=datetime(2025, 1, 6), end_date=datetime(2025, 1, 13)
            ),
        }
        pretty_print_query_dates(query_dates_dict)
        captured = capsys.readouterr()
        assert "ID 0: Start = 2025-01-05, End = 2025-01-12" in captured.out
        assert "ID 1: Start = 2025-01-06, End = 2025-01-13" in captured.out
