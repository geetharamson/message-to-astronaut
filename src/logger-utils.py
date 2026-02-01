# src/logger_utils.py

import csv
import os
from datetime import datetime
from typing import Dict

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
EVENTS_FILE = os.path.join(DATA_DIR, "iss_events.csv")

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def init_csv_if_needed():
    ensure_data_dir()
    if not os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp_utc",
                "user_name",
                "user_message",
                "iss_lat",
                "iss_long",
                "distance_km",
                "event_type"
            ])

def log_event(event: Dict):
    """Append an event row to the CSV file."""
    init_csv_if_needed()
    with open(EVENTS_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            event.get("timestamp_utc"),
            event.get("user_name"),
            event.get("user_message"),
            event.get("iss_lat"),
            event.get("iss_long"),
            event.get("distance_km"),
            event.get("event_type"),
        ])

def create_event_record(user_name: str, user_message: str,
                        iss_lat: float, iss_long: float,
                        distance_km: float, event_type: str) -> Dict:
    return {
        "timestamp_utc": datetime.utcnow().isoformat(),
        "user_name": user_name,
        "user_message": user_message,
        "iss_lat": iss_lat,
        "iss_long": iss_long,
        "distance_km": round(distance_km, 2),
        "event_type": event_type,
    }
