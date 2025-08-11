import pytest
import json
from datetime import datetime
from aita.core.query_dates import generate_query_dates
from aita.core.filters import Filters


def load_test_vectors():
    """
    Load test vectors from the JSON file.
    """
    with open("test/test_query_dates.json", "r") as f:
        test_vectors = json.load(f)

    # Convert JSON data into Python objects
    for vector in test_vectors:
        vector["filter_obj"] = Filters(**vector["filter_obj"])
    return test_vectors


# Load test vectors
test_vectors = load_test_vectors()


@pytest.mark.parametrize("test_vector", test_vectors)
def test_generate_query_dates(test_vector):
    """
    Test generate_query_dates using test vectors.
    """
    filter_obj = test_vector["filter_obj"]
    expected_combinations = test_vector["expected_combinations"]
    first_query = test_vector["first_query"]
    last_query = test_vector["last_query"]

    # Generate query dates
    query_dates = generate_query_dates(filter_obj)

    # Validate the number of combinations
    assert (
        len(query_dates) == expected_combinations
    ), "Incorrect number of QueryDates generated"

    # Validate the first QueryDates
    first_generated_query = query_dates[0]
    assert first_generated_query.start_date == datetime.strptime(
        first_query["start_date"], "%d %B %Y"
    ), "First QueryDates start_date mismatch"
    assert first_generated_query.end_date == datetime.strptime(
        first_query["end_date"], "%d %B %Y"
    ), "First QueryDates end_date mismatch"

    # Validate the last QueryDates
    last_generated_query = query_dates[len(query_dates) - 1]
    assert last_generated_query.start_date == datetime.strptime(
        last_query["start_date"], "%d %B %Y"
    ), "Last QueryDates start_date mismatch"
    assert last_generated_query.end_date == datetime.strptime(
        last_query["end_date"], "%d %B %Y"
    ), "Last QueryDates end_date mismatch"


def test_generate_query_dates_missing_parameters():
    """
    Test that generate_query_dates raises a ValueError for missing parameters.
    """
    # Create a Filters object with missing parameters
    filter_obj = Filters(
        start_date=None,
        flexibility=2,
        duration_min=3,
        duration_max=5,
    )

    # Expect a ValueError
    with pytest.raises(
        ValueError,
        match="Filters object must have start_date, flexibility, duration_min, and duration_max defined.",
    ):
        generate_query_dates(filter_obj)


def test_generate_query_dates_edge_case():
    """
    Test generate_query_dates with edge case values (e.g., flexibility = 0, duration_min = duration_max).
    """
    # Create a Filters object with edge case values
    filter_obj = Filters(
        start_date="15 December",
        flexibility=0,
        duration_min=5,
        duration_max=5,
    )

    # Generate query dates
    query_dates = generate_query_dates(filter_obj)

    # Expected number of combinations: 1 (no flexibility, single duration)
    assert (
        len(query_dates) == 1
    ), "Incorrect number of QueryDates generated for edge case"

    # Validate the single QueryDates
    single_query = query_dates[0]
    assert single_query.start_date == datetime.strptime("15 December 2025", "%d %B %Y")
    assert single_query.end_date == datetime.strptime("20 December 2025", "%d %B %Y")
