# src/main.py

import time

from iss_tracker import get_iss_position, haversine_distance_km
from location_utils import get_city_coordinates
from logger_utils import create_event_record, log_event

from config import (CITY_LAT, CITY_LONG, CITY_NAME, DISTANCE_THRESHOLD_KM,
                    POLL_INTERVAL_SECONDS, USER_MESSAGE, USER_NAME)


def initialize_user_inputs():
    global USER_NAME, USER_MESSAGE, CITY_NAME, CITY_LAT, CITY_LONG

    USER_NAME = input("Enter your name: ").strip()
    USER_MESSAGE = input("Enter the message you want to send: ").strip()
    CITY_NAME = input("Enter your city name: ").strip()

    print(f"Fetching coordinates for {CITY_NAME}...")
    CITY_LAT, CITY_LONG = get_city_coordinates(CITY_NAME)
    print(f"City coordinates: {CITY_LAT}, {CITY_LONG}")

def run_cli_tracker():
    initialize_user_inputs()

    print(f"\nTracking ISS for city: {CITY_NAME}")
    print(f"Your message: {USER_MESSAGE}")
    print("-" * 60)

    while True:
        try:
            iss_lat, iss_long = get_iss_position()
            distance = haversine_distance_km(CITY_LAT, CITY_LONG, iss_lat, iss_long)

            print(f"ISS at ({iss_lat:.2f}, {iss_long:.2f}) | Distance: {distance:.1f} km")

            if distance < DISTANCE_THRESHOLD_KM:
                print("\n🛰️ ISS is above your city!")
                print(f"📤 Sending your message: {USER_MESSAGE}")

                event = create_event_record(
                    USER_NAME, USER_MESSAGE, iss_lat, iss_long, distance, "message_sent"
                )
                log_event(event)

                reply = f"Hello {USER_NAME}! I see {CITY_NAME} from up here!"
                print("📥 Astronaut reply:", reply)

                reply_event = create_event_record(
                    USER_NAME, reply, iss_lat, iss_long, distance, "astronaut_reply"
                )
                log_event(reply_event)
                break

            time.sleep(POLL_INTERVAL_SECONDS)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    run_cli_tracker()
