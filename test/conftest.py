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


def pytest_ignore_collect(collection_path: Path, config):
    """
    Ignore test files not marked as applicable in applicable_tests.json,
    using categories and an excluded list.
    """
    # Only process .py test files
    if collection_path.suffix != ".py":
        return False

    # Get path relative to test folder
    test_folder = Path(__file__).parent.resolve()
    rel_path = str(collection_path.relative_to(test_folder)).replace("\\", "/")

    # Load applicable tests config
    try:
        with open(APPLICABLE_TESTS_PATH, encoding="utf-8") as f:
            config_data = json.load(f)
    except Exception as e:
        print(f"Warning: Could not load applicable_tests.json: {e}")
        return False

    tests_to_run = config_data.get("tests_to_run", {})
    excluded_tests = set(
        config_data.get("excluded", [])
    )  # now a list → set for fast lookup

    # Always exclude if in the excluded list
    if rel_path in excluded_tests:
        return True

    # Check all enabled categories
    for category, enabled in tests_to_run.items():
        if enabled:
            category_tests = config_data.get(category, {})
            if category_tests.get(rel_path, False):
                return False  # Found in an enabled category → include it

    # If not found in any enabled category → ignore
    return True
