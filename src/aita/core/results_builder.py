from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ResultsAirports:
    """
    Represents ...
    """

    id: str
    airport_name: str


def pretty_print_results_airports(results_airports: dict[int, ResultsAirports]) -> None:
    """
    Nicely prints all entries in a dict[int, ResultsAirports].
    """
    for key, airport in results_airports.items():
        print(f"ID {key}: id = {airport.id}, airport_name = {airport.airport_name}")


@dataclass
class ResultsFlights:
    """
    Represents ...
    """

    airline_name: str
    flight_numbers: str
    departure_time: str
    arrival_time: str
    duration: str
    stops: int
    price: float
    currency: str


def pretty_print_results_flights(results_flights: dict[int, ResultsFlights]) -> None:
    """
    Prints ResultsFlights entries in a table format with aligned columns.
    """
    # Define table headers
    headers = [
        "ID",
        "Airline",
        "Flight #",
        "Departure",
        "Arrival",
        "Duration",
        "Stops",
        "Price",
        "Currency",
    ]

    # Calculate column widths dynamically
    col_widths = {h: len(h) for h in headers}

    for idx, flight in results_flights.items():
        col_widths["ID"] = max(col_widths["ID"], len(str(idx)))
        col_widths["Airline"] = max(col_widths["Airline"], len(flight.airline_name))
        col_widths["Flight #"] = max(col_widths["Flight #"], len(flight.flight_numbers))
        col_widths["Departure"] = max(
            col_widths["Departure"],
            len(datetime.fromisoformat(flight.departure_time).strftime("%H:%M")),
        )
        col_widths["Arrival"] = max(
            col_widths["Arrival"],
            len(datetime.fromisoformat(flight.arrival_time).strftime("%H:%M")),
        )
        col_widths["Duration"] = max(col_widths["Duration"], len(flight.duration))
        col_widths["Stops"] = max(col_widths["Stops"], len(str(flight.stops)))
        col_widths["Price"] = max(col_widths["Price"], len(f"{flight.price:.2f}"))
        col_widths["Currency"] = max(col_widths["Currency"], len(flight.currency))

    # Create format string
    row_format = (
        f"{{:<{col_widths['ID']}}}  "
        f"{{:<{col_widths['Airline']}}}  "
        f"{{:<{col_widths['Flight #']}}}  "
        f"{{:<{col_widths['Departure']}}}  "
        f"{{:<{col_widths['Arrival']}}}  "
        f"{{:<{col_widths['Duration']}}}  "
        f"{{:>{col_widths['Stops']}}}  "
        f"{{:>{col_widths['Price']}}}  "
        f"{{:<{col_widths['Currency']}}}"
    )

    # Print header
    print(row_format.format(*headers))
    print("-" * (sum(col_widths.values()) + 2 * (len(headers) - 1)))

    # Print rows
    for idx, flight in results_flights.items():
        print(
            row_format.format(
                idx,
                flight.airline_name,
                flight.flight_numbers,
                datetime.fromisoformat(flight.departure_time).strftime("%H:%M"),
                datetime.fromisoformat(flight.arrival_time).strftime("%H:%M"),
                flight.duration,
                flight.stops,
                f"{flight.price:.2f}",
                flight.currency,
            )
        )
