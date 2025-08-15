from __future__ import annotations
import json
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Optional


@dataclass
class ResultAirport:
    """
    Represents ...
    """

    id: str
    airport_name: str


def pretty_print_result_airports(results_airports: dict[int, ResultAirport]) -> None:
    """
    Nicely prints all entries in a dict[int, ResultAirport].
    """
    for key, airport in results_airports.items():
        print(f"ID {key}: id = {airport.id}, airport_name = {airport.airport_name}")


@dataclass
class ResultFlight:
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


def pretty_print_result_flights(result_flights: dict[int, ResultFlight]) -> None:
    """
    Prints ResultFlight entries in a table format with aligned columns.
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

    for idx, flight in result_flights.items():
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
    for idx, flight in result_flights.items():
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


# todo: find a different way to save results
def save_result_flights(
    result_flights: dict[int, ResultFlight], log_file_name: str
) -> None:
    # Convert dataclasses to dicts and keys to strings
    json_ready = {str(k): asdict(v) for k, v in result_flights.items()}

    # Save to JSON file
    with open(log_file_name, "w", encoding="utf-8") as f:
        json.dump(json_ready, f, indent=2)


@dataclass
class Result:
    """
    Represents ...
    """

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    origin: Optional[str] = None
    destination: Optional[str] = None
    origin_airport: ResultAirport = field(default_factory=ResultAirport)
    destination_airport: ResultAirport = field(default_factory=ResultAirport)
    flight: ResultFlight = field(default_factory=ResultFlight)

    @classmethod
    def from_results(
        cls,
        start_date: datetime,
        end_date: datetime,
        origin: str,
        destination: str,
        origin_airport: ResultAirport,
        destination_airport: ResultAirport,
        flight: ResultFlight,
    ) -> Result:
        return cls(
            start_date=start_date,
            end_date=end_date,
            origin=origin,
            destination=destination,
            origin_airport=origin_airport,
            destination_airport=destination_airport,
            flight=flight,
        )


def pretty_print_result(results: dict[int, Result]) -> None:
    """
    Prints Result entries in a table format with aligned columns.
    """
    headers = [
        "ID",
        # "Start Date",
        # "End Date",
        "Origin",
        "Ori ID",
        "Destination",
        "Dest ID",
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

    for idx, res in results.items():
        # Dates
        start_str = res.start_date.strftime("%Y-%m-%d") if res.start_date else ""
        end_str = res.end_date.strftime("%Y-%m-%d") if res.end_date else ""

        col_widths["ID"] = max(col_widths["ID"], len(str(idx)))
        # col_widths["Start Date"] = max(col_widths["Start Date"], len(start_str))
        # col_widths["End Date"] = max(col_widths["End Date"], len(end_str))

        # Origin & Destination
        col_widths["Origin"] = max(col_widths["Origin"], len(res.origin or ""))
        col_widths["Ori ID"] = max(col_widths["Ori ID"], len(res.origin_airport.id))
        col_widths["Destination"] = max(
            col_widths["Destination"], len(res.destination or "")
        )
        col_widths["Dest ID"] = max(
            col_widths["Dest ID"], len(res.destination_airport.id)
        )

        # Flight details
        col_widths["Airline"] = max(col_widths["Airline"], len(res.flight.airline_name))
        col_widths["Flight #"] = max(
            col_widths["Flight #"], len(res.flight.flight_numbers)
        )
        col_widths["Departure"] = max(
            col_widths["Departure"],
            len(datetime.fromisoformat(res.flight.departure_time).strftime("%H:%M")),
        )
        col_widths["Arrival"] = max(
            col_widths["Arrival"],
            len(datetime.fromisoformat(res.flight.arrival_time).strftime("%H:%M")),
        )
        col_widths["Duration"] = max(col_widths["Duration"], len(res.flight.duration))
        col_widths["Stops"] = max(col_widths["Stops"], len(str(res.flight.stops)))
        col_widths["Price"] = max(col_widths["Price"], len(f"{res.flight.price:.2f}"))
        col_widths["Currency"] = max(col_widths["Currency"], len(res.flight.currency))

    # Create format string
    row_format = (
        f"{{:<{col_widths['ID']}}}  "
        # f"{{:<{col_widths['Start Date']}}}  "
        # f"{{:<{col_widths['End Date']}}}  "
        f"{{:<{col_widths['Origin']}}}  "
        f"{{:<{col_widths['Ori ID']}}}  "
        f"{{:<{col_widths['Destination']}}}  "
        f"{{:<{col_widths['Dest ID']}}}  "
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
    for idx, res in results.items():
        start_str = res.start_date.strftime("%Y-%m-%d") if res.start_date else ""
        end_str = res.end_date.strftime("%Y-%m-%d") if res.end_date else ""

        print(
            row_format.format(
                idx,
                # start_str,
                # end_str,
                res.origin or "",
                res.origin_airport.id,
                res.destination or "",
                res.destination_airport.id,
                res.flight.airline_name,
                res.flight.flight_numbers,
                datetime.fromisoformat(res.flight.departure_time).strftime("%H:%M"),
                datetime.fromisoformat(res.flight.arrival_time).strftime("%H:%M"),
                res.flight.duration,
                res.flight.stops,
                f"{res.flight.price:.2f}",
                res.flight.currency,
            )
        )
