"""[Priceline COM](https://rapidapi.com/ntd119/api/priceline-com2)"""

import os
import requests
import json
from aita.core.query_builder import QueryFlights
from aita.core.results_builder import (
    ResultAirport,
    ResultFlight,
    Result,
    pretty_print_result_airports,
    pretty_print_result_flights,
    save_result_flights,
)

try:
    from dotenv import load_dotenv
except ImportError:
    print("Missing 'python-dotenv'. Please install with: pip install python-dotenv")
    exit(1)


LOG: bool = True  # Set to False to disable logging
USE_LOG: bool = True  # Set to True to use log files instead of API calls
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def search_flights(query_flights: QueryFlights) -> dict[int, Result]:
    # todo update this format
    log_dates = (
        query_flights.query_dates.start_date.strftime("%Y-%m-%d")
        + "_"
        + query_flights.query_dates.end_date.strftime("%Y-%m-%d")
    )

    # auto-complete: Origin
    response_json = _search_flights_priceline_com2_auto_complete(
        query_flights.origin,
        log=LOG,
        log_name=query_flights.origin + "_" + log_dates,
        use_log=USE_LOG,
    )
    origin_airports = _generate_result_airports(response_json)

    # print("\nOrigin Airports found:", len(origin_airports))
    # pretty_print_result_airports(origin_airports)

    # auto-complete: Destination
    response_json = _search_flights_priceline_com2_auto_complete(
        query_flights.destination,
        log=LOG,
        log_name=query_flights.destination + "_" + log_dates,
        use_log=USE_LOG,
    )
    destination_airports = _generate_result_airports(response_json)

    # print("\nDestination Airports found:", len(destination_airports))
    # pretty_print_result_airports(destination_airports)  # Debugging output

    if not origin_airports:
        raise ValueError("No origin airports found.")
    if not destination_airports:
        raise ValueError("No destination airports found.")

    # todo: for the moment it always use the first airport found
    response_json = _search_flights_priceline_com2_search_roundtrip(
        originAirportCode=origin_airports[0].id,
        destinationAirportCode=destination_airports[0].id,
        departureDate=query_flights.query_dates.start_date.strftime("%Y-%m-%d"),
        returnDate=query_flights.query_dates.end_date.strftime("%Y-%m-%d"),
        direct_flight=query_flights.flight.direct,
        log=LOG,
        log_name=log_dates,
        use_log=USE_LOG,
    )

    result_flights: dict[int, ResultFlight] = _generate_result_flights(response_json)
    log_name = (
        f"flights_{query_flights.origin}_{query_flights.destination}_{log_dates}.json"
    )
    log_path = os.path.join(BASE_DIR, f"flights_api_priceline_com2_{log_name}.json")
    save_result_flights(result_flights, log_path)
    # print("\nResult Flights:", len(result_flights))
    # pretty_print_result_flights(result_flights)  # Debugging output

    results: dict[int, Result] = {}
    for idx, result_flight in result_flights.items():
        restult = Result.from_results(
            query_flights.query_dates.start_date,
            query_flights.query_dates.end_date,
            query_flights.origin,
            query_flights.destination,
            origin_airports[0],
            destination_airports[0],
            result_flight,
        )
        results[idx] = restult

    return results


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


def _search_flights_priceline_com2(
    type: str,
    query: dict,
    log: bool = False,
    log_name: str = "",
    use_log: bool = False,
) -> dict:
    load_dotenv()

    # Check keys required
    missing_keys = check_env_keys(REQUIRED_KEYS)
    if missing_keys:
        raise RuntimeError(f"Missing keys in .env file: {missing_keys}")

    # Get API base URL and key from environment variables
    base_url = os.getenv("FLIGHT_API_BASE_URL")
    api_key = os.getenv("FLIGHT_API_KEY")

    if not base_url or not api_key:
        raise RuntimeError("Flight API base URL or API key not set in environment.")

    headers = {
        "x-rapidapi-key": f"{api_key}",
        "x-rapidapi-host": "priceline-com2.p.rapidapi.com",
    }

    log_path = os.path.join(
        BASE_DIR, f"flights_api_priceline_com2_{type}_{log_name}.json"
    )
    try:
        if use_log:
            with open(log_path, "r", encoding="utf-8") as f:
                response_json = json.load(f)
        else:
            # Make the API request to auto-complete
            response = requests.get(
                f"{base_url}/{type}",
                params=query,
                headers=headers,
            )
            response.raise_for_status()
            response_json = response.json()

            if log:
                with open(log_path, "w", encoding="utf-8") as f:
                    json.dump(response_json, f, ensure_ascii=False, indent=2)

        return response_json

    except requests.RequestException as e:
        print(f"Flight API request failed: {e}")
        return {}
    except Exception as e:
        print(f"Flight API request failed: {e}")
        return {}


def _search_flights_priceline_com2_auto_complete(
    query: str, log: bool = False, log_name: str = "", use_log: bool = False
) -> dict:
    # Prepare query dictionary
    query = {"query": query}

    response_json = _search_flights_priceline_com2(
        type="auto-complete",
        query=query,
        log=log,
        log_name=log_name,
        use_log=use_log,
    )
    return response_json


def _search_flights_priceline_com2_search_roundtrip(
    originAirportCode: str,
    destinationAirportCode: str,
    departureDate: str,
    returnDate: str,
    direct_flight: bool,
    log: bool = False,
    log_name: str = "",
    use_log: bool = False,
) -> dict:
    # Prepare query dictionary
    query = {
        "originAirportCode": originAirportCode,
        "destinationAirportCode": destinationAirportCode,
        "departureDate": departureDate,
        "returnDate": returnDate,
        "numOfStops": "0" if direct_flight else "1",
    }

    response_json = _search_flights_priceline_com2(
        type="search-roundtrip",
        query=query,
        log=log,
        log_name=log_name,
        use_log=use_log,
    )

    return response_json


def _generate_result_airports(response_json: dict) -> dict[int, ResultAirport]:
    """
    Returns a dict[int, ResultAirport] containing all airports
    where cityName matches entered (case-insensitive).
    """
    results_airports = {}
    data = response_json.get("data", {})
    search_items = data.get("searchItems", [])
    idx = 0
    for item in search_items:
        if (
            item.get("type") == "AIRPORT"
            and item.get("cityName", "").lower() == item.get("entered", "").lower()
        ):
            results_airports[idx] = ResultAirport(
                id=item["id"], airport_name=item["itemName"]
            )
            idx += 1
    return results_airports


# def _filter_flights(
#     response_json: dict, origin_code: str, destination_code: str, departure_date: str
# ) -> list:
#     """
#     Filters listings for flights matching the given origin, destination, and departure date.
#     """
#     filtered = []
#     for listing in response_json.get("data", {}).get("listings", []):
#         if not listing.get("slices"):
#             continue
#         # For roundtrip, you may want to check both outbound and inbound slices
#         outbound_slice = listing["slices"][0]
#         segments = outbound_slice.get("segments", [])
#         if not segments:
#             continue
#         first_segment = segments[0]
#         last_segment = segments[-1]
#         # Get codes and dates
#         seg_depart_code = (
#             first_segment.get("departInfo", {}).get("airport", {}).get("code")
#         )
#         seg_arrive_code = (
#             last_segment.get("arrivalInfo", {}).get("airport", {}).get("code")
#         )
#         seg_depart_time = (
#             first_segment.get("departInfo", {}).get("time", {}).get("dateTime", "")
#         )
#         seg_depart_date = seg_depart_time[:10]  # 'YYYY-MM-DD'
#         # Filter by codes and date
#         if (
#             seg_depart_code == origin_code
#             and seg_arrive_code == destination_code
#             and seg_depart_date == departure_date
#             and len(segments) == 1  # Only direct flights
#         ):
#             filtered.append(listing)
#         # Check inbound slice for return date, etc.
#         if len(listing["slices"]) > 1:
#             inbound_slice = listing["slices"][1]
#             inbound_segments = inbound_slice.get("segments", [])
#             if not inbound_segments:
#                 continue
#             first_inbound_segment = inbound_segments[0]
#             last_inbound_segment = inbound_segments[-1]
#             # Get return codes and dates
#             seg_arrive_code_return = (
#                 first_inbound_segment.get("arrivalInfo", {})
#                 .get("airport", {})
#                 .get("code")
#             )
#             seg_depart_code_return = (
#                 last_inbound_segment.get("departInfo", {})
#                 .get("airport", {})
#                 .get("code")
#             )
#             seg_arrive_time_return = (
#                 first_inbound_segment.get("arrivalInfo", {})
#                 .get("time", {})
#                 .get("dateTime", "")
#             )
#             seg_arrive_date_return = seg_arrive_time_return[:10]  # 'YYYY-MM-DD'
#             # Filter by return codes and date
#             if (
#                 seg_depart_code_return == destination_code
#                 and seg_arrive_code_return == origin_code
#                 and seg_arrive_date_return == departure_date
#                 and len(inbound_segments) == 1  # Only direct flights
#             ):
#                 filtered.append(listing)
#     return filtered


def _generate_result_flights(response_json: dict) -> dict[int, ResultFlight]:
    result_flights: dict[int, ResultFlight] = {}

    data = response_json.get("data", {})
    listings = data.get("listings", [])
    airline_lookup = {a.get("code"): a.get("name") for a in data.get("airline", [])}

    for idx, listing in enumerate(listings):
        # Airline names
        marketing_airlines = listing.get("marketingAirlines", [])
        airline_names = [
            airline_lookup.get(ma.get("code"), ma.get("code"))
            for ma in marketing_airlines
        ]
        airline_name_str = ", ".join(filter(None, airline_names)) or "Unknown Airline"

        # Initialize fields
        flight_numbers = []
        departure_time = ""
        arrival_time = ""
        total_duration_minutes = 0
        total_stops = 0

        slices = listing.get("slices", [])
        if slices:
            # Outbound departure time = first segment's depart time of first slice
            first_slice_segments = slices[0].get("segments", [])
            if first_slice_segments:
                departure_time = (
                    first_slice_segments[0]
                    .get("departInfo", {})
                    .get("time", {})
                    .get("dateTime", "")
                )

            # Inbound arrival time = last segment's arrival time of last slice
            last_slice_segments = slices[-1].get("segments", [])
            if last_slice_segments:
                arrival_time = (
                    last_slice_segments[-1]
                    .get("arrivalInfo", {})
                    .get("time", {})
                    .get("dateTime", "")
                )

            # Gather flight numbers, stops, and total duration
            for slice_info in slices:
                segs = slice_info.get("segments", [])
                total_stops += max(len(segs) - 1, 0)
                for seg in segs:
                    fn = seg.get("flightNumber")
                    if fn:
                        flight_numbers.append(str(fn))
                dur_str = slice_info.get("durationInMinutes")
                if dur_str and dur_str.isdigit():
                    total_duration_minutes += int(dur_str)

        # Format duration
        duration_str = (
            f"{total_duration_minutes // 60}h {total_duration_minutes % 60}m"
            if total_duration_minutes
            else "N/A"
        )
        flight_numbers_str = ", ".join(flight_numbers)

        # Price & currency
        price = None
        currency = None
        fare_brands = listing.get("fareBrands", [])
        if fare_brands:
            for p in fare_brands[0].get("price", []):
                if p.get("type") == "TOTAL_PRICE":
                    price = p.get("amount")
                    currency = p.get("currencyCode")
                    break
        if price is None:
            tpwd = listing.get("totalPriceWithDecimal", {})
            price = tpwd.get("price")
        if not currency:
            currency = "USD"

        result_flights[idx] = ResultFlight(
            airline_name=airline_name_str,
            flight_numbers=flight_numbers_str,
            departure_time=departure_time,
            arrival_time=arrival_time,
            duration=duration_str,
            stops=total_stops,
            price=price if price is not None else 0.0,
            currency=currency,
        )

    return result_flights
