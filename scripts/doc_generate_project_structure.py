#!/usr/bin/env python

"""
Generate a markdown file representing the folder and file structure of the
AitA project, with directories listed before files and a tree-like visual
format using ├── and └── connectors.

The script:
- Recursively walks through the AitA project directory.
- Skips specified folders and files listed in SKIP_LIST.
- Prints directories first, then files, preserving the filesystem's natural order.
- Outputs the structure into a markdown file at 'aita/docs/project_structure.md',
  wrapped inside a YAML code block for formatting.

Usage:
    Run this script from the root of the repository or using the relative path:
        ./scripts/generate_structure.py

Adjust SKIP_LIST to exclude any additional files or folders you do not want
to appear in the generated tree structure.

Output example snippet:
AitA/
├── docs
│   ├── README.md
│   └── ...
├── src
│   ├── main.py
│   └── ...
└── LICENSE
"""

import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
PROJECT_DIR = os.path.join(ROOT_DIR, "AitA")
OUTPUT_FILE = os.path.join(ROOT_DIR, "aita", "docs", "project_structure.md")

# 🔥 Names to skip (folders or files)
SKIP_LIST = {".git", ".temp", "__pycache__", ".pytest_cache"}


def write_tree(path, prefix="", is_last=True, output_lines=None):
    if output_lines is None:
        output_lines = []

    try:
        entries = [e for e in os.listdir(path) if e not in SKIP_LIST]
    except PermissionError:
        return output_lines

    # Separate directories and files
    dirs = [e for e in entries if os.path.isdir(os.path.join(path, e))]
    files = [e for e in entries if os.path.isfile(os.path.join(path, e))]
    ordered_entries = dirs + files  # folders first, then files

    entries_count = len(ordered_entries)

    for index, entry in enumerate(ordered_entries):
        full_path = os.path.join(path, entry)
        is_entry_last = index == entries_count - 1
        connector = "└──" if is_entry_last else "├──"

        output_lines.append(f"{prefix}{connector} {entry}")

        if os.path.isdir(full_path):
            next_prefix = f"{prefix}    " if is_entry_last else f"{prefix}│   "
            write_tree(
                full_path,
                prefix=next_prefix,
                is_last=is_entry_last,
                output_lines=output_lines,
            )

    return output_lines


def main():
    os.makedirs(os.path.join(ROOT_DIR, "docs"), exist_ok=True)

    lines = ["# 🔧 Project Structure", "", "```yaml", "AitA/"]
    tree_lines = write_tree(PROJECT_DIR)
    lines.extend(tree_lines)
    lines.append("```")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"✅ Project structure written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
