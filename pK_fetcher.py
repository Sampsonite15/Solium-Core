"""
pK Index Tracker - Real-Time Geomagnetic Variability Monitor

This module fetches real-time planetary K-index data from NOAA's Space
Weather Prediction Center and logs H-component variability (deltaB)
for estimating provisional K (pK) values.

GitHub Source: https://github.com/Sampsonite15/Solium-Core
Last Edited: 2026-06-12
Author: Andrew

Related Modules:
  - DeltaB_Rolling_Log.py (Rolling log for historic field values)
  - DeltaB Calculator.py (Computes real-time H deltas)
  - Kp Tracker.py (Optional NOAA Kp cross-check)

Requires:
  - Python 3.10+
  - requests
"""

import requests
from datetime import datetime, timezone
from DeltaB_Rolling_Log import log_reading, prune_old_data

# NOAA Space Weather Prediction Center - 1-minute Kp feed
DATA_URL = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"

# K-index alert thresholds
KP_THRESHOLDS = {
    5: "🟡 G1 MINOR STORM",
    6: "🟠 G2 MODERATE STORM",
    7: "🔴 G3 STRONG STORM",
    8: "🔴 G4 SEVERE STORM",
    9: "🚨 G5 EXTREME STORM"
}

def get_storm_level(kp):
    """Returns storm alert string for a given Kp value, or None if quiet."""
    for threshold in sorted(KP_THRESHOLDS.keys(), reverse=True):
        if kp >= threshold:
            return KP_THRESHOLDS[threshold]
    return None

def fetch_pk_data():
    """
    Fetches the latest 1-minute planetary K-index data from NOAA.
    Logs each reading and prunes old data from the rolling log.
    Returns a list of parsed reading dicts.
    """
    try:
        response = requests.get(DATA_URL, timeout=10)
        response.raise_for_status()
        raw_data = response.json()
    except Exception as e:
        print(f"⚠️ Failed to fetch pK data: {e}")
        return []

    readings = []
    for entry in raw_data:
        try:
            timestamp_str = entry["time_tag"]
            kp_value = float(entry["kp_index"])

            readings.append({
                "station": "PLANETARY",
                "timestamp": timestamp_str,
                "kp": kp_value,
                "H": kp_value  # proxy for deltaB logging compatibility
            })

            log_reading("PLANETARY", timestamp_str, kp_value)

        except Exception as e:
            print(f"⚠️ Skipping entry due to error: {e}")

    prune_old_data()
    return readings

def display_pk_summary(readings):
    """Prints a summary of the most recent Kp reading and storm status."""
    if not readings:
        print("⚠️ No pK data available.")
        return

    latest = readings[-1]
    kp = latest["kp"]
    timestamp = latest["timestamp"]
    storm = get_storm_level(kp)

    border = "=" * 40
    print(f"\n{border}")
    print("🌍  PLANETARY K-INDEX REPORT".center(40))
    print(f"{border}")
    print(f"Latest Kp:      {kp}")
    print(f"Timestamp:      {timestamp} UTC")
    print(f"Readings logged: {len(readings)}")

    if storm:
        print(f"\n{storm}")
    else:
        print(f"\n🟢 Geomagnetic conditions quiet")

    print(f"{border}")

if __name__ == "__main__":
    readings = fetch_pk_data()
    display_pk_summary(readings)
