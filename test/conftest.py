import subprocess
import json
import os
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from aita.version import get_version

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
    - If a file is mapped to True in an enabled category → keep all test cases in it.
    - If a file is mapped to a list → keep only listed test cases.
    - An empty list → skip all test cases in that file.
    - "excluded" always takes priority and removes test files.

    It runs the test files in the order they are defined in applicable_tests.json.
    """
    config_data = load_applicable_tests()
    tests_to_run = config_data.get("tests_to_run", {})
    excluded_tests = set(config_data.get("excluded", []))

    # Build map of file_path -> allowed tests (None = all, set = selected, [] = none)
    allowed_tests_map = {}
    disabled_files = set()

    for category, enabled in tests_to_run.items():
        category_tests = config_data.get(category, {})
        for file_path, entry in category_tests.items():
            if enabled:
                if isinstance(entry, bool) and entry:
                    allowed_tests_map[file_path] = None
                elif isinstance(entry, list):
                    allowed_tests_map[file_path] = set(entry) if entry else []
            else:
                # Category is disabled → all its files should be deselected
                disabled_files.add(file_path)

    if not allowed_tests_map and not excluded_tests and not disabled_files:
        return  # Nothing to filter

    test_folder = Path(__file__).parent.resolve()
    items_by_file = {}
    deselected = []

    # Group items by file, applying filtering rules
    for item in items:
        file_path = Path(item.location[0]).resolve()
        try:
            rel_path = str(file_path.relative_to(test_folder)).replace("\\", "/")
        except ValueError:
            rel_path = file_path.name  # fallback

        # Exclude files first
        if rel_path in excluded_tests or rel_path in disabled_files:
            deselected.append(item)
            continue

        allowed = allowed_tests_map.get(rel_path)

        if allowed is None:
            items_by_file.setdefault(rel_path, []).append(item)
        elif isinstance(allowed, set) and item.name in allowed:
            items_by_file.setdefault(rel_path, []).append(item)
        else:
            # empty list or not in allowed set → deselect
            deselected.append(item)

    # Reorder according to allowed_tests_map order
    new_items = [
        item for f in allowed_tests_map.keys() for item in items_by_file.get(f, [])
    ]

    if deselected:
        config.hook.pytest_deselected(items=deselected)
    items[:] = new_items
