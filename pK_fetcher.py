"""
pK Index Tracker - Real-Time Geomagnetic Variability Monitor

This module fetches magnetometer data from a remote relay (JSON format)
and processes it for H-component variability (deltaB), suitable for
estimating provisional K (pK) values per observatory.

GitHub Source: https://github.com/<your-username>/<your-repo-name>
Last Edited: 2025-06-17
Author: Andrew

Related Modules:
  - DeltaB_Rolling_Log.py (Rolling log for historic field values)
  - DeltaB Calculator.py (Computes real-time H deltas)
  - Kp Tracker.py (Optional NOAA Kp cross-check)

Requires:
  - Python 3.10+
  - requests
"""

# ⬇️ Your imports and code begin here
from DeltaB_Rolling_Log import log_reading, prune_old_data
import json
import requests
from datetime import datetime

# Constants
DATA_URL = "https://example-observatory-feed/data/latest.json"
OBSERVATORIES = ["BOU", "FRD", "CMO"]  # Add or adjust as needed

def fetch_magnetometer_data():
    response = requests.get(DATA_URL)
    response.raise_for_status()
    data = response.json()

    readings = []
    for station in data["stations"]:
        if station["code"] in OBSERVATORIES:
            readings.append({
                "station": station["code"],
                "timestamp": datetime.strptime(station["timestamp"], "%Y-%m-%dT%H:%M:%SZ"),
                "H": station["H"],
                "D": station["D"],
                "Z": station["Z"]
            })
    for reading in readings:
      log_reading(
          reading["station"],
          reading["timestamp"],
          reading["H"]
    )
    prune_old_data()
    return readings
if __name__ == "__main__":
    readings = fetch_magnetometer_data()
    print(readings)  # Optional: sanity check
