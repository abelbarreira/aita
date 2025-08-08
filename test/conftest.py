import subprocess
import os
from datetime import datetime
from aita.version import get_version


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
