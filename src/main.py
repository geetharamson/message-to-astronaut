# src/main.py

import time

from iss_tracker import get_iss_position, haversine_distance_km
from logger_utils import create_event_record, log_event

from config import (DISTANCE_THRESHOLD_KM, MY_LAT, MY_LONG,
                    POLL_INTERVAL_SECONDS, USER_MESSAGE, USER_NAME)


def run_cli_tracker():
    print("Tracking ISS... waiting for it to fly near your city.")
    print(f"User: {USER_NAME}")
    print(f"Message: {USER_MESSAGE}")
    print("-" * 60)

    while True:
        try:
            iss_lat, iss_long = get_iss_position()
            distance = haversine_distance_km(MY_LAT, MY_LONG, iss_lat, iss_long)

            print(f"ISS at ({iss_lat:.2f}, {iss_long:.2f}) | Distance: {distance:.1f} km")

            if distance < DISTANCE_THRESHOLD_KM:
                print("\n🛰️ ISS is above your city!")
                print(f"📤 Sending your message: {USER_MESSAGE}")
                event = create_event_record(
                    USER_NAME, USER_MESSAGE, iss_lat, iss_long, distance, "message_sent"
                )
                log_event(event)
                time.sleep(2)
                reply = f"📥 Astronaut replies: Hello {USER_NAME}! I see your city from up here!"
                print(reply)
                reply_event = create_event_record(
                    USER_NAME, reply, iss_lat, iss_long, distance, "astronaut_reply"
                )
                log_event(reply_event)
                break

            time.sleep(POLL_INTERVAL_SECONDS)

        except Exception as e:
            print(f"Error while tracking ISS: {e}")
            time.sleep(POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    run_cli_tracker()
