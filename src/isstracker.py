# src/iss_tracker.py

from math import atan2, cos, radians, sin, sqrt
from typing import Tuple

import requests

ISS_API_URL = "http://api.open-notify.org/iss-now.json"

def get_iss_position() -> Tuple[float, float]:
    """Fetch current ISS latitude and longitude from the API."""
    response = requests.get(ISS_API_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    iss_lat = float(data["iss_position"]["latitude"])
    iss_long = float(data["iss_position"]["longitude"])
    return iss_lat, iss_long

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates using the Haversine formula."""
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c
