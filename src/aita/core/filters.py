from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class FlightFilter:
    """
    Represents a flight filter with its details.
    """

    departure_time_min: Optional[str] = None
    departure_time_max: Optional[str] = None
    direct: Optional[bool] = None


@dataclass
class HotelFilter:
    """
    Represents a hotel filter with its details.
    """

    stars: Optional[int] = None
    all_inclusive: Optional[bool] = None
    distance_to_beach: Optional[float] = None


@dataclass
class Filter:
    """
    Represents a filter with a name and a list of values.
    """

    origin: Optional[str] = None
    destination: Optional[str] = None
    area: Optional[str] = None
    start_date: Optional[str] = None
    duration_min: Optional[int] = None
    duration_max: Optional[int] = None
    flexibility: Optional[int] = None
    flight: FlightFilter = field(default_factory=FlightFilter)
    hotel: HotelFilter = field(default_factory=HotelFilter)

    @classmethod
    def from_prompt(cls, prompt: str) -> Filter:
        """
        Parses a natural language prompt and returns a populated Filter instance.
        """
        # Initialize the filter object
        filter_instance = cls()

        # Match origin and destination
        if match := re.search(
            r"\bfrom\s+([A-Za-z\s]+?)\s+to\s+([A-Za-z\s]+?)(?:,|\.|$)",
            prompt,
            re.IGNORECASE,
        ):
            filter_instance.origin = match.group(1).strip()
            filter_instance.destination = match.group(2).strip()

        # Match area
        if match := re.search(r'area\s+"?([A-Za-z\s]+)"?', prompt, re.IGNORECASE):
            filter_instance.area = match.group(1).strip()

        # Match start date
        if match := re.search(
            r"starting from\s+\"?([A-Za-z0-9\s]+?)\s+(January|February|March|April|May|June|July|August|September|October|November|December)\"?(?:,|\s|$)",
            prompt,
            re.IGNORECASE,
        ):
            filter_instance.start_date = (
                f"{match.group(1).strip()} {match.group(2).strip()}"
            )

        # Match flexibility
        if match := re.search(
            r"flexibility of\s+\"?(\d+)\"?\s+days?", prompt, re.IGNORECASE
        ):
            filter_instance.flexibility = int(match.group(1))

        # Match duration
        if match := re.search(
            r"staying between\s+\"?(\d+)\"?\s+to\s+\"?(\d+)\"?\s+days",
            prompt,
            re.IGNORECASE,
        ):
            filter_instance.duration_min, filter_instance.duration_max = map(
                int, match.groups()
            )

        # Match hotel proximity
        if match := re.search(
            r"within\s+\"?([\d.]+)\s*(m|meters|km|kilometers)\"?\s+(from the beach|from the city center)",
            prompt,
            re.IGNORECASE,
        ):
            distance, unit = match.groups()[:2]
            distance = float(distance)
            if unit.lower() in ["km", "kilometers"]:
                distance *= 1000  # Convert kilometers to meters
            filter_instance.hotel.distance_to_beach = distance

        # Match hotel stars
        if match := re.search(r"\"?(\d+)\"?\s+stars?", prompt, re.IGNORECASE):
            filter_instance.hotel.stars = int(match.group(1))

        # Match board type
        if re.search(r"\bAll[- ]Inclusive\b", prompt, re.IGNORECASE):
            filter_instance.hotel.all_inclusive = True
        else:
            filter_instance.hotel.all_inclusive = (
                False  # Explicitly set to False if not found
            )

        # Match flight departure time
        if match := re.search(
            r"departing between\s+\"?([\d:apm\s]+)\"?\s+and\s+\"?([\d:apm\s]+)\"?",
            prompt,
            re.IGNORECASE,
        ):
            filter_instance.flight.departure_time_min = match.group(1).strip()
            filter_instance.flight.departure_time_max = match.group(2).strip()

        # Match direct flights
        if re.search(r"\bdirect\b", prompt, re.IGNORECASE):
            filter_instance.flight.direct = True
        else:
            filter_instance.flight.direct = (
                False  # Explicitly set to False if not found
            )

        return filter_instance

    def matches(self, other: Filter) -> bool:
        """
        Compares this Filter instance with another Filter instance to check if they match.
        """
        # Compare basic attributes
        if self.origin and other.origin and self.origin != other.origin:
            return False
        if (
            self.destination
            and other.destination
            and self.destination != other.destination
        ):
            return False
        if self.area and other.area and self.area != other.area:
            return False
        if self.start_date and other.start_date and self.start_date != other.start_date:
            return False

        # Compare duration
        if (
            self.duration_min
            and other.duration_min
            and self.duration_min > other.duration_min
        ):
            return False
        if (
            self.duration_max
            and other.duration_max
            and self.duration_max < other.duration_max
        ):
            return False

        # Compare flight filters
        if self.flight.departure_time_min and other.flight.departure_time_min:
            if self.flight.departure_time_min != other.flight.departure_time_min:
                return False
        if self.flight.departure_time_max and other.flight.departure_time_max:
            if self.flight.departure_time_max != other.flight.departure_time_max:
                return False
        if (
            self.flight.direct
            and other.flight.direct
            and self.flight.direct != other.flight.direct
        ):
            return False

        # Compare hotel filters
        if (
            self.hotel.stars
            and other.hotel.stars
            and self.hotel.stars != other.hotel.stars
        ):
            return False
        if self.hotel.all_inclusive and other.hotel.all_inclusive:
            if self.hotel.all_inclusive != other.hotel.all_inclusive:
                return False
        if self.hotel.distance_to_beach and other.hotel.distance_to_beach:
            if self.hotel.distance_to_beach < other.hotel.distance_to_beach:
                return False

        # If all checks pass, the filters match
        return True

    def check_missing_filters(self) -> list[str]:
        """
        Checks if any filter in the Filter instance are None and returns a list of missing attributes.
        """
        missing = []

        # Check top-level attributes
        for attr in [
            "origin",
            "destination",
            "area",
            "start_date",
            "duration_min",
            "duration_max",
            "flexibility",
        ]:
            if getattr(self, attr) is None:
                missing.append(attr)

        # Check nested flight attributes
        for attr in ["departure_time_min", "departure_time_max", "direct"]:
            if getattr(self.flight, attr) is None:
                missing.append(f"flight.{attr}")

        # Check nested hotel attributes
        for attr in ["stars", "all_inclusive", "distance_to_beach"]:
            if getattr(self.hotel, attr) is None:
                missing.append(f"hotel.{attr}")

        return missing
