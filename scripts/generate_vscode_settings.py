"""
This script detects the Python interpreter path of the current Hatch environment
(named "default") and updates the VS Code workspace settings file
(.vscode/settings.json) to set "python.defaultInterpreterPath" accordingly.

This ensures that VS Code uses the correct Python interpreter for features
like linting, IntelliSense, and debugging, without requiring manual configuration.

If the settings file already contains the correct path, no changes are made.
"""

import json
import os
import subprocess
from pathlib import Path


def get_hatch_python_path():
    """Get the Python interpreter path from the current Hatch environment."""
    try:
        result = subprocess.run(
            ["hatch", "env", "find", "default"],
            capture_output=True,
            text=True,
            check=True,
        )
        path = result.stdout.strip()
        if os.name == "nt":
            return str(Path(path) / "Scripts" / "python.exe")
        else:
            return str(Path(path) / "bin" / "python")
    except subprocess.CalledProcessError as e:
        print(f"❌  Hatch environment not found: {e}")
        return None
    except Exception as e:
        print(f"❌  Unexpected error finding Hatch environment: {e}")
        return None


def update_vscode_settings(python_path):
    """Create or update .vscode/settings.json with the correct python interpreter path."""
    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)

    settings_path = vscode_dir / "settings.json"

    settings = {}
    if settings_path.exists():
        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                settings = json.load(f)
        except json.JSONDecodeError:
            print(
                "⚠️  Invalid JSON in .vscode/settings.json. Please fix it before running this script."
            )
            return

    current_path = settings.get("python.defaultInterpreterPath")
    if current_path == python_path:
        print(f"ℹ️  VS Code interpreter already set to: {python_path}")
        return

    settings["python.defaultInterpreterPath"] = python_path

    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)

    print(f"✅  VS Code interpreter updated to: {python_path}")


if __name__ == "__main__":
    python_path = get_hatch_python_path()
    if python_path:
        update_vscode_settings(python_path)
