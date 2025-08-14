"""[Priceline COM](https://rapidapi.com/ntd119/api/priceline-com2)"""

import os
import requests
import json
from aita.core.query_builder import QueryFlights
from aita.core.results_builder import ResultsAirports, pretty_print_results_airports

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def search_flights(query_flights: QueryFlights) -> dict:

    # auto-complete: Origin
    response_json = _search_flights_priceline_com2_auto_complete(
        query_flights.origin, log=True, log_name=query_flights.origin, use_log=True
    )
    origin_airports = _generate_result_airports(response_json)

    print("\nOrigin Airports found:", len(origin_airports))
    pretty_print_results_airports(origin_airports)

    # auto-complete: Destination
    response_json = _search_flights_priceline_com2_auto_complete(
        query_flights.destination,
        log=True,
        log_name=query_flights.destination,
        use_log=True,
    )
    destination_airports = _generate_result_airports(response_json)

    print("\nDestination Airports found:", len(destination_airports))
    pretty_print_results_airports(destination_airports)  # Debugging output

    if not origin_airports:
        raise ValueError("No origin airports found.")
    if not destination_airports:
        raise ValueError("No destination airports found.")

    response_json = _search_flights_priceline_com2_search_roundtrip(
        originAirportCode=origin_airports[0].id,
        destinationAirportCode=destination_airports[0].id,
        departureDate=query_flights.query_dates.start_date.strftime("%Y-%m-%d"),
        returnDate=query_flights.query_dates.end_date.strftime("%Y-%m-%d"),
        direct_flight=query_flights.flight.direct,
        log=True,
        log_name="",
        use_log=True,
    )

    filtered = _filter_flights(
        response_json,
        origin_airports[0].id,
        destination_airports[0].id,
        query_flights.query_dates.start_date.strftime("%Y-%m-%d"),
    )

    print(f"Found {len(filtered)} matching flights.")
    for flight in filtered:
        print(flight["totalPriceWithDecimal"]["price"])

    return response_json  # Return the full JSON response


def _search_flights_priceline_com2(
    type: str,
    query: dict,
    log: bool = False,
    log_name: str = "",
    use_log: bool = False,
) -> dict:
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

    # currency = response_json.get("data", {}).get("currency")
    # print(currency)

    return response_json


def _generate_result_airports(response_json: dict) -> dict[int, ResultsAirports]:
    """
    Returns a dict[int, ResultsAirports] containing all airports
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
            results_airports[idx] = ResultsAirports(
                id=item["id"], airport_name=item["itemName"]
            )
            idx += 1
    return results_airports


def _filter_flights(
    response_json: dict, origin_code: str, destination_code: str, departure_date: str
) -> list:
    """
    Filters listings for flights matching the given origin, destination, and departure date.
    """
    filtered = []
    for listing in response_json.get("data", {}).get("listings", []):
        if not listing.get("slices"):
            continue
        # For roundtrip, you may want to check both outbound and inbound slices
        outbound_slice = listing["slices"][0]
        segments = outbound_slice.get("segments", [])
        if not segments:
            continue
        first_segment = segments[0]
        last_segment = segments[-1]
        # Get codes and dates
        seg_depart_code = (
            first_segment.get("departInfo", {}).get("airport", {}).get("code")
        )
        seg_arrive_code = (
            last_segment.get("arrivalInfo", {}).get("airport", {}).get("code")
        )
        seg_depart_time = (
            first_segment.get("departInfo", {}).get("time", {}).get("dateTime", "")
        )
        seg_depart_date = seg_depart_time[:10]  # 'YYYY-MM-DD'
        # Filter by codes and date
        if (
            seg_depart_code == origin_code
            and seg_arrive_code == destination_code
            and seg_depart_date == departure_date
            and len(segments) == 1  # Only direct flights
        ):
            filtered.append(listing)
        # Check inbound slice for return date, etc.
        if len(listing["slices"]) > 1:
            inbound_slice = listing["slices"][1]
            inbound_segments = inbound_slice.get("segments", [])
            if not inbound_segments:
                continue
            first_inbound_segment = inbound_segments[0]
            last_inbound_segment = inbound_segments[-1]
            # Get return codes and dates
            seg_arrive_code_return = (
                first_inbound_segment.get("arrivalInfo", {})
                .get("airport", {})
                .get("code")
            )
            seg_depart_code_return = (
                last_inbound_segment.get("departInfo", {})
                .get("airport", {})
                .get("code")
            )
            seg_arrive_time_return = (
                first_inbound_segment.get("arrivalInfo", {})
                .get("time", {})
                .get("dateTime", "")
            )
            seg_arrive_date_return = seg_arrive_time_return[:10]  # 'YYYY-MM-DD'
            # Filter by return codes and date
            if (
                seg_depart_code_return == destination_code
                and seg_arrive_code_return == origin_code
                and seg_arrive_date_return == departure_date
                and len(inbound_segments) == 1  # Only direct flights
            ):
                filtered.append(listing)
    return filtered
