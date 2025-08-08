import pytest
import json
from src.aita.core.prompt_parser import parse_prompt


def load_test_cases():
    with open("test/test_prompt_parser.json", "r") as f:
        return json.load(f)


@pytest.mark.parametrize("test_case", load_test_cases())
def test_prompt_parsing(test_case):
    prompt = test_case["prompt"]
    expected = test_case["expected"]
    result = parse_prompt(prompt)

    for key, expected_val in expected.items():
        actual_val = result.get(key)

        if isinstance(expected_val, dict):
            assert isinstance(actual_val, dict), f"{key} should be a dict"
            for subkey, subval in expected_val.items():
                assert (
                    actual_val.get(subkey) == subval
                ), f"{key}.{subkey} mismatch: expected {subval}, got {actual_val.get(subkey)}"
        else:
            assert (
                actual_val == expected_val
            ), f"{key} mismatch: expected {expected_val}, got {actual_val}"
