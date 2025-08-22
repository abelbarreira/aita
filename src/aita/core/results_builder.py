from __future__ import annotations

from dataclasses import dataclass


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
