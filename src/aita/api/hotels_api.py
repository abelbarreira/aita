"""
Hotels API: Handles communication with external hotel API.
"""

import os
import requests


def search_hotels(query: dict) -> list:
    base_url = os.getenv("HOTEL_API_BASE_URL")
    api_key = os.getenv("HOTEL_API_KEY")

    if not base_url or not api_key:
        raise RuntimeError("Hotel API base URL or API key not set in environment.")

    try:
        response = requests.get(
            f"{base_url}/search",
            params=query,
            headers={"Authorization": f"Bearer {api_key}"},
        )
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.RequestException as e:
        print(f"Hotel API request failed: {e}")
        return []
