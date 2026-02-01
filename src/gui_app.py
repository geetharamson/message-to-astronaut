# src/gui_app.py

import threading
import time
import tkinter as tk
from tkinter import messagebox

from iss_tracker import get_iss_position, haversine_distance_km
from logger_utils import create_event_record, log_event

from config import (DISTANCE_THRESHOLD_KM, MY_LAT, MY_LONG,
                    POLL_INTERVAL_SECONDS, USER_MESSAGE, USER_NAME)


class ISSGuiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Message to the Astronaut")

        self.status_label = tk.Label(root, text="Click 'Start Tracking' to begin.", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.message_label = tk.Label(root, text=f"Your message: {USER_MESSAGE}", font=("Arial", 10))
        self.message_label.pack(pady=5)

        self.start_button = tk.Button(root, text="Start Tracking", command=self.start_tracking)
        self.start_button.pack(pady=10)

        self.stop_flag = False

    def start_tracking(self):
        self.stop_flag = False
        self.status_label.config(text="Tracking ISS... waiting for it to fly near your city.")
        self.start_button.config(state=tk.DISABLED)
        thread = threading.Thread(target=self.track_iss_loop, daemon=True)
        thread.start()

    def track_iss_loop(self):
        while not self.stop_flag:
            try:
                iss_lat, iss_long = get_iss_position()
                distance = haversine_distance_km(MY_LAT, MY_LONG, iss_lat, iss_long)

                status_text = f"ISS at ({iss_lat:.2f}, {iss_long:.2f}) | Distance: {distance:.1f} km"
                self.update_status(status_text)

                if distance < DISTANCE_THRESHOLD_KM:
                    self.handle_iss_overhead(iss_lat, iss_long, distance)
                    break

                time.sleep(POLL_INTERVAL_SECONDS)

            except Exception as e:
                self.update_status(f"Error: {e}")
                time.sleep(POLL_INTERVAL_SECONDS)

        self.start_button.config(state=tk.NORMAL)

    def handle_iss_overhead(self, iss_lat, iss_long, distance):
        self.update_status("🛰️ ISS is above your city!")
        event = create_event_record(
            USER_NAME, USER_MESSAGE, iss_lat, iss_long, distance, "message_sent"
        )
        log_event(event)

        reply = f"Hello {USER_NAME}! I see your city from up here!"
        reply_event = create_event_record(
            USER_NAME, reply, iss_lat, iss_long, distance, "astronaut_reply"
        )
        log_event(reply_event)

        messagebox.showinfo("Astronaut Reply", reply)

    def update_status(self, text):
        self.status_label.config(text=text)

def main():
    root = tk.Tk()
    app = ISSGuiApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
