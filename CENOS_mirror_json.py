
import requests
import json
import os
from datetime import datetime, timezone
from mirror_to_json import mirror_to_json
from dedupe_cenos import dedupe

# ---------- Config ----------

OUTPUT_FILE = "cenos_data.json"
NASA_URL = "https://api.nasa.gov/neo/rest/v1/feed"
API_KEY = "DEMO_KEY"  # Replace with your NASA API key

# ---------- Core Functions ----------

def fetch_neos():
    """Fetches today's NEO data from NASA and returns formatted entries."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    params = {
        "start_date": today,
        "end_date": today,
        "api_key": API_KEY
    }

    try:
        response = requests.get(NASA_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        neos_today = data["near_earth_objects"][today]
    except Exception as e:
        print(f"⚠️ Failed to fetch NEO data: {e}")
        return []

    entries = []
    for neo in neos_today:
        try:
            name = neo["name"]
            approach_date = neo["close_approach_data"][0]["close_approach_date"]
            miss_distance_km = float(neo["close_approach_data"][0]["miss_distance"]["kilometers"])
            velocity_km_s = float(neo["close_approach_data"][0]["relative_velocity"]["kilometers_per_second"])
            magnitude = neo["absolute_magnitude_h"]

            entries.append({
                "name": name,
                "approach_date": approach_date,
                "miss_distance_km": round(miss_distance_km, 0),
                "velocity_km_s": round(velocity_km_s, 2),
                "magnitude": magnitude
            })

        except Exception as e:
            print(f"⚠️ Skipping NEO due to error: {e}")

    return entries

def save_to_json(entries):
    """Appends new NEO entries to the existing JSON log."""
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r') as f:
                existing = json.load(f)
        except json.JSONDecodeError:
            existing = []
    else:
        existing = []

    combined = existing + entries

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(combined, f, indent=2)

    print(f"💾 Saved {len(entries)} new entries to {OUTPUT_FILE}")

# ---------- Main Execution ----------

if __name__ == "__main__":
    border = "=" * 40
    print(f"\n{border}")
    print("🛰️  CENOS MIRROR JSON".center(40))
    print(f"{border}")

    entries = fetch_neos()

    if entries:
        save_to_json(entries)
        mirror_to_json(OUTPUT_FILE)
        dedupe()
        print(f"\n✅ Pipeline complete: {len(entries)} NEOs logged, mirrored, and deduped.")
    else:
        print("⚠️ No NEO entries to log.")

    print(f"{border}")
