# src/location_utils.py

import requests


def get_city_coordinates(city_name: str):
    """Use OpenStreetMap Nominatim API to convert city name to coordinates."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city_name, "format": "json", "limit": 1}

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    if not data:
        raise ValueError(f"City '{city_name}' not found.")

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    return lat, lon