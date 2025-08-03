"""
Main entry point for AitA - AI Travel Assistant
"""

import argparse
from app.core.prompt_parser import parse_prompt
from app.version import get_version


def main():
    parser = argparse.ArgumentParser(description="🧳 AitA - AI Travel Assistant")
    parser.add_argument("--prompt", type=str, help="Travel prompt in natural language")
    parser.add_argument(
        "--version", action="store_true", help="Show the current version"
    )

    args = parser.parse_args()

    if args.version:
        print(f"AitA Version: {get_version()}")
        return

    if args.prompt:
        filters = parse_prompt(args.prompt)
        print("Parsed Filters:")
        for key, val in filters.items():
            print(f"{key}: {val}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
