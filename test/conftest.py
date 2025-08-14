import subprocess
import json
import os
from datetime import datetime
from aita.version import get_version

# Set the path to applicable_tests.json here (can be outside test folder)
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
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
        return commit
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


def pytest_ignore_collect(collection_path: "pathlib.Path", config):
    """
    Ignore test files not marked as applicable in applicable_tests.json.
    """
    # Only check .py files in the test folder
    if not str(collection_path).endswith(".py"):
        return False

    # Get relative path from test folder
    test_folder = os.path.abspath(os.path.dirname(__file__))
    rel_path = os.path.relpath(str(collection_path), test_folder).replace("\\", "/")

    # Load applicable tests config
    try:
        with open(APPLICABLE_TESTS_PATH, encoding="utf-8") as f:
            applicable = json.load(f)
    except Exception as e:
        print(f"Warning: Could not load applicable_tests.json: {e}")
        return False

    return not applicable.get(rel_path, False)
