import subprocess
import json
import os
from datetime import datetime
from aita.version import get_version
from pathlib import Path

# Path to applicable_tests.json (can be overridden by env var)
APPLICABLE_TESTS_PATH = os.environ.get(
    "APPLICABLE_TESTS_PATH",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "applicable_tests.json")),
)


def load_applicable_tests():
    try:
        with open(APPLICABLE_TESTS_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"\n\nWarning: Could not load applicable_tests.json: {e}\n\n")


def get_git_branch():
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
            .decode()
            .strip()
        )
    except Exception:
        return "Unknown"


def get_git_commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    except Exception:
        return "Unknown"


def pytest_html_report_title(report):
    report.title = f"AitA {get_version()} Test Report"


def pytest_html_results_summary(prefix, summary, postfix):
    branch = get_git_branch()
    commit = get_git_commit()
    # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # ci = os.getenv("CI", "false")

    prefix.extend(
        [
            f"<br>",
            f"<p>Branch: <b>{branch}</b></p>",  # creates a separate paragraph (line)
            f"<p>Git commit: <b>{commit}</b></p>",
            # f"<p>Timestamp: {timestamp}</p>",
            # f"<p>CI run: {ci}</p>",
            f"<br>",
        ]
    )


def pytest_collection_modifyitems(config, items):
    """
    Filter test files and specific test cases based on applicable_tests.json.

    Rules:
    - If a file is mapped to True in an enabled category → keep all tests cases in it.
    - If a file is mapped to a list → keep only listed tests cases.
    - An empty list → skip all tests cases in that file.
    - "excluded" always takes priority and removes tests files
    """
    config_data = load_applicable_tests()
    tests_to_run = config_data.get("tests_to_run", {})
    excluded_tests = set(config_data.get("excluded", []))

    # Build map of file_path -> tests to allow (None = all, set = specific tests, [] = none)
    allowed_tests_map = {}

    # Check all enabled categories
    for category, enabled in tests_to_run.items():
        if not enabled:
            continue
        category_tests = config_data.get(category, {})
        for file_path, entry in category_tests.items():
            if isinstance(entry, bool) and entry:
                allowed_tests_map[file_path] = None  # None = allow all tests
            elif isinstance(entry, list):
                allowed_tests_map[file_path] = (
                    set(entry) if entry else []
                )  # empty list = no tests

    if not allowed_tests_map and not excluded_tests:
        return  # No filtering needed

    test_folder = Path(__file__).parent.resolve()
    new_items = []
    deselected = []

    for item in items:
        file_path = Path(item.location[0]).resolve()
        try:
            rel_path = str(file_path.relative_to(test_folder)).replace("\\", "/")
        except ValueError:
            rel_path = file_path.name  # fallback

        # Always exclude first
        if rel_path in excluded_tests:
            deselected.append(item)
            continue

        allowed_cases_for_file = allowed_tests_map.get(rel_path)

        if allowed_cases_for_file is None:
            # None = all tests allowed
            new_items.append(item)
        elif isinstance(allowed_cases_for_file, set):
            # Only specific tests allowed
            if item.name in allowed_cases_for_file:
                new_items.append(item)
            else:
                deselected.append(item)
        elif allowed_cases_for_file == []:
            # Empty list → skip all tests in this file
            deselected.append(item)
        else:
            # File not listed anywhere → deselect
            deselected.append(item)

    if deselected:
        config.hook.pytest_deselected(items=deselected)
        items[:] = new_items
