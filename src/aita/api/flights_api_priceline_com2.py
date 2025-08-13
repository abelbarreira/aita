""" """

import os
import requests
import json
from aita.core.query_builder import QueryFlights
from aita.core.results_builder import ResultsAirports, pretty_print_results_airports


# [Priceline COM](https://rapidapi.com/ntd119/api/priceline-com2)
def search_flights_priceline_com2_auto_complete(
    base_url: str, api_key: str, query_param: str
) -> dict:
    query = {"query": query_param}

    headers = {
        "x-rapidapi-key": f"{api_key}",
        "x-rapidapi-host": "priceline-com2.p.rapidapi.com",
    }

    # try:
    #     response = requests.get(
    #         f"{base_url}/auto-complete",
    #         params=query,
    #         headers=headers,
    #     )
    #     response.raise_for_status()
    #     response_json = response.json()

    #     # Save the JSON response to a file
    #     with open(
    #         f"flights_api_priceline_com2_auto_complete_{query_param}.json",
    #         "w",
    #         encoding="utf-8",
    #     ) as f:
    #         json.dump(response_json, f, ensure_ascii=False, indent=2)

    # except requests.RequestException as e:
    #     print(f"Flight API request failed: {e}")
    #     return

    try:
        # Instead of making the API request, load the response from file
        with open(
            f"flights_api_priceline_com2_auto_complete_{query_param}.json",
            "r",
            encoding="utf-8",
        ) as f:
            response_json = json.load(f)

    except Exception as e:
        print(f"Flight API request failed: {e}")
        return

    return response_json  # Return the full JSON response


def search_flights_priceline_com2_search_roundtrip(
    base_url: str,
    api_key: str,
    originAirportCode: str,
    destinationAirportCode: str,
    departureDate: str,
    returnDate: str,
) -> dict:
    query = {
        "originAirportCode": originAirportCode,
        "destinationAirportCode": destinationAirportCode,
        "departureDate": departureDate,
        "returnDate": returnDate,
    }

    print(query)

    headers = {
        "x-rapidapi-key": f"{api_key}",
        "x-rapidapi-host": "priceline-com2.p.rapidapi.com",
    }

    # try:
    #     response = requests.get(
    #         f"{base_url}/search-roundtrip",
    #         params=query,
    #         headers=headers,
    #     )
    #     response.raise_for_status()
    #     response_json = response.json()

    #     # Save the JSON response to a file
    #     with open(
    #         "flights_api_priceline_com2_search_roundtrip.json", "w", encoding="utf-8"
    #     ) as f:
    #         json.dump(response_json, f, ensure_ascii=False, indent=2)

    # except requests.RequestException as e:
    #     print(f"Flight API request failed: {e}")
    #     return

    try:
        # Instead of making the API request, load the response from file
        with open(
            "flights_api_priceline_com2_search_roundtrip.json", "r", encoding="utf-8"
        ) as f:
            response_json = json.load(f)

    except Exception as e:
        print(f"Flight API request failed: {e}")
        return

    return response_json  # Return the full JSON response


def search_flights_priceline_com2(query_flights: QueryFlights) -> dict:
    base_url = os.getenv("FLIGHT_API_BASE_URL")
    api_key = os.getenv("FLIGHT_API_KEY")

    if not base_url or not api_key:
        raise RuntimeError("Flight API base URL or API key not set in environment.")

    # auto-complete: Origin
    response_json = search_flights_priceline_com2_auto_complete(
        base_url, api_key, query_flights.origin
    )

    origin_airports = generate_result_airports(response_json)
    print("\nAirports found:", len(origin_airports))
    pretty_print_results_airports(origin_airports)  # Debugging output

    # auto-complete: Destination
    response_json = search_flights_priceline_com2_auto_complete(
        base_url, api_key, query_flights.destination
    )

    destination_airports = generate_result_airports(response_json)
    print("\nAirports found:", len(destination_airports))
    pretty_print_results_airports(destination_airports)  # Debugging output

    response_json = search_flights_priceline_com2_search_roundtrip(
        base_url=base_url,
        api_key=api_key,
        originAirportCode=origin_airports[0].id,
        destinationAirportCode=destination_airports[0].id,
        departureDate=query_flights.query_dates.start_date.strftime("%Y-%m-%d"),
        returnDate=query_flights.query_dates.end_date.strftime("%Y-%m-%d"),
    )

    print("\nSearch results:")
    print(response_json)
    return response_json  # Return the full JSON response


def generate_result_airports(response_json: dict) -> dict[int, ResultsAirports]:
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
