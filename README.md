# Message to the Astronaut 🚀

A playful Python project that tracks the International Space Station (ISS) in real time and "sends" a message when it flies near Maynooth, Ireland. When the ISS is overhead, the astronaut "replies"—and the interaction is logged for analysis and visualization in Power BI.

## Features

- **Real-time ISS tracking** using a public API
- **Distance calculation** with the Haversine formula
- **CLI and GUI** (Tkinter) interfaces
- **Event logging to CSV** for analytics
- **Power BI-ready dataset** for visual storytelling

## Tech stack

- **Python** (requests, Tkinter, standard library)
- **Data logging:** CSV
- **Visualization:** Power BI (optional, see `docs/powerbi_guide.md`)

## Project structure

```text
src/
  main.py          # CLI tracker
  gui_app.py       # GUI tracker
  iss_tracker.py   # ISS API + distance logic
  config.py        # Configuration
  logger_utils.py  # CSV logging
data/
  iss_events.csv   # Logged events
docs/
  architecture.md
  sequence_diagram.md
  powerbi_guide.md


message-to-astronaut/
├─ src/
│  ├─ main.py              # Core ISS tracking & message logic (CLI)
│  ├─ gui_app.py           # Tkinter GUI version
│  ├─ iss_tracker.py       # ISS API + distance logic
│  ├─ config.py            # Config (location, thresholds, message)
│  └─ logger_utils.py      # Logging to CSV for Power BI
├─ data/
│  └─ iss_events.csv       # Logged ISS-overhead events
├─ docs/
│  ├─ architecture.md      # Detailed design notes
│  ├─ sequence_diagram.md  # Mermaid sequence diagram
│  └─ powerbi_guide.md     # Steps to build the Power BI report
├─ README.md
├─ requirements.txt
└─ .gitignore
