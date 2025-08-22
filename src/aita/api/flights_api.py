"""
Flights API: Handles communication with external flight API.
"""

import os

import requests


def search_flights(query: dict) -> list:
    base_url = os.getenv("FLIGHT_API_BASE_URL")
    api_key = os.getenv("FLIGHT_API_KEY")

    if not base_url or not api_key:
        raise RuntimeError("Flight API base URL or API key not set in environment.")

    try:
        response = requests.get(
            f"{base_url}/search",
            params=query,
            headers={"Authorization": f"Bearer {api_key}"},
        )
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.RequestException as e:
        print(f"Flight API request failed: {e}")
        return []
