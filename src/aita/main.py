#!/usr/bin/env python

"""
Main entry point for AitA - AI Travel Assistant
"""

import argparse
import os
from aita.version import get_version
from aita.core.filters import Filters
from aita.core.query_dates import (
    generate_query_dates,
    pretty_print_query_dates,
    QueryDates,
)

try:
    from dotenv import load_dotenv
except ImportError:
    print("Missing 'python-dotenv'. Please install with: pip install python-dotenv")
    exit(1)

REQUIRED_KEYS = [
    "CURRENCY",
    "FLIGHT_API_BASE_URL",
    "FLIGHT_API_KEY",
    "HOTEL_API_BASE_URL",
    "HOTEL_API_KEY",
]


def check_env_keys(required_keys):
    missing = []
    for key in required_keys:
        if not os.getenv(key):
            missing.append(key)
    return missing


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

    # If --version is not provided, require --prompt
    if not args.prompt:
        print("Error: --prompt is required unless --version is specified.\n")
        parser.print_help()
        exit(1)

    # Load environment variables from .env file
    load_dotenv()

    # Check keys required
    missing_keys = check_env_keys(REQUIRED_KEYS)
    if missing_keys:
        print("Missing keys in .env file:")
        for key in missing_keys:
            print(f" - {key}")
        exit(1)
    print("All required .env keys are present.")

    # Parse prompt
    filters: Filters = Filters.from_prompt(args.prompt)
    print("\nParsed Filters:")
    filters.pretty_print()

    # Generate query dates
    print("\nQuery Dates:")
    query_dates: dict[int, QueryDates] = generate_query_dates(filters)
    pretty_print_query_dates(query_dates)


if __name__ == "__main__":
    main()
