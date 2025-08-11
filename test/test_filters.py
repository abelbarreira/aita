import pytest
import json
from src.aita.core.filters import Filters


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
