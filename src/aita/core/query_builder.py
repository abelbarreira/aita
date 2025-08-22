"""
Query Builder: Converts structured filters into API query parameters.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from aita.core.filters import Filters, FlightFilters, HotelFilters
from aita.core.query_dates import QueryDates


@dataclass
class QueryFlights:
    """
    Represents a query flights.
    """

    query_dates: QueryDates
    origin: Optional[str] = None
    destination: Optional[str] = None
    flight: FlightFilters = field(default_factory=FlightFilters)

    @classmethod
    def from_filters(cls, filters: Filters, query_dates: QueryDates) -> QueryFlights:
        return cls(
            query_dates=query_dates,
            origin=filters.origin,
            destination=filters.destination,
            flight=filters.flight,
        )

    def build_query_flights(self) -> dict:
        return {
            "origin": self.origin,
            "destination": self.destination,
            "start_date": self.query_dates.start_date.strftime("%Y-%m-%d"),
            "end_date": self.query_dates.end_date.strftime("%Y-%m-%d"),
            "departure_time_min": self.flight.departure_time_min,
            "departure_time_max": self.flight.departure_time_max,
            "direct": self.flight.direct,
        }

    def pretty_print(self) -> None:
        """
        Nicely prints all attributes of the QueryFlights instance.
        """
        print(f"\n{self.__class__.__name__}:")
        print(f"  origin: {self.origin}")
        print(f"  destination: {self.destination}")
        print(f"  start_date: {self.query_dates.start_date.strftime('%Y-%m-%d')}")
        print(f"  end_date: {self.query_dates.end_date.strftime('%Y-%m-%d')}")
        print(f"  departure_time_min: {self.flight.departure_time_min}")
        print(f"  departure_time_max: {self.flight.departure_time_max}")
        print(f"  direct: {self.flight.direct}")


@dataclass
class QueryHotels:
    """
    Represents a query hotels.
    """

    query_dates: QueryDates
    destination: Optional[str] = None
    area: Optional[str] = None
    hotel: HotelFilters = field(default_factory=HotelFilters)

    @classmethod
    def from_filters(cls, filters: Filters, query_dates: QueryDates) -> QueryHotels:
        return cls(
            query_dates=query_dates,
            destination=filters.destination,
            area=filters.area,
            hotel=filters.hotel,
        )

    def build_query_hotels(self) -> dict:
        return {
            "destination": self.destination,
            "area": self.area,
            "start_date": self.query_dates.start_date.strftime("%Y-%m-%d"),
            "end_date": self.query_dates.end_date.strftime("%Y-%m-%d"),
            "stars": self.hotel.stars,
            "all_inclusive": self.hotel.all_inclusive,
            "distance_to_beach": self.hotel.distance_to_beach,
        }

    def pretty_print(self) -> None:
        """
        Nicely prints all attributes of the QueryHotels instance.
        """
        print(f"{self.__class__.__name__}:")
        print(f"  destination: {self.destination}")
        print(f"  area: {self.area}")
        print(f"  start_date: {self.query_dates.start_date.strftime('%Y-%m-%d')}")
        print(f"  end_date: {self.query_dates.end_date.strftime('%Y-%m-%d')}")
        print(f"  stars: {self.hotel.stars}")
        print(f"  all_inclusive: {self.hotel.all_inclusive}")
