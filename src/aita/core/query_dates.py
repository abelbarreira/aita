from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Dict
from datetime import datetime, timedelta
from aita.core.filters import Filters


@dataclass
class QueryDates:
    """
    Represents a query date range with a start and end date.
    """

    start_date: datetime
    end_date: datetime


def generate_query_dates(filter_obj: Filters) -> Dict[int, QueryDates]:
    """
    Generates a dictionary of QueryDates keyed by ID based on the Filters parameters.

    Args:
        filter_obj (Filters): The filter object containing date-related parameters.

    Returns:
        Dict[int, QueryDates]: A dictionary of QueryDates keyed by ID.
    """
    if (
        filter_obj.start_date is None
        or filter_obj.flexibility is None
        or filter_obj.duration_min is None
        or filter_obj.duration_max is None
    ):
        raise ValueError(
            "Filters object must have start_date, flexibility, duration_min, and duration_max defined."
        )

    # Remove ordinal suffixes from day (e.g., '5th' -> '5')
    start_date_clean = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", filter_obj.start_date)
    start_date_str = f"{start_date_clean} 2025"
    start_date = datetime.strptime(start_date_str, "%d %B %Y")
    flexibility = filter_obj.flexibility
    duration_min = filter_obj.duration_min
    duration_max = filter_obj.duration_max

    query_dates = {}
    query_id = 0

    # Generate all combinations of start_date and end_date
    for flex_offset in range(-flexibility, flexibility + 1):
        flex_start_date = start_date + timedelta(days=flex_offset)
        for duration in range(duration_min, duration_max + 1):
            end_date = flex_start_date + timedelta(days=duration)
            query_dates[query_id] = QueryDates(
                start_date=flex_start_date, end_date=end_date
            )
            query_id += 1

    return query_dates


def pretty_print_query_dates(query_dates: Dict[int, QueryDates]) -> None:
    """
    Nicely prints all entries in a Dict[int, QueryDates].
    """
    for key, qd in query_dates.items():
        print(
            f"ID {key}: Start = {qd.start_date.strftime('%Y-%m-%d')}, End = {qd.end_date.strftime('%Y-%m-%d')}"
        )
