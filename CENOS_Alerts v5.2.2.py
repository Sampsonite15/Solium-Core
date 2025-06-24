import requests
import os
import math
from datetime import datetime
import pytz
import json
from pathlib import Path
from mirror_to_json import mirror_to_json

# ---------- Core Functions ----------
def mirror_to_json(neo_path, path="neo_alert_log.json"):
    mirror_data = {
        "name": neo.get("name"),
        "neo_reference_id": neo.get("neo_reference_id"),
        "ars": neo.get("ars"),
        "tier": neo.get("tier"),
        "timestamp_local": neo.get("timestamp_local"),
        "hazardous": neo.get("is_potentially_hazardous_asteroid"),
        "composition": neo.get("composition", "Unknown"),
        "resource_flag": neo.get("resource_flag", False)
    }

def estimate_mass(diameter_km):
    radius_m = (diameter_km * 1000) / 2
    volume_m3 = (4/3) * math.pi * (radius_m ** 3)
    density_kg_per_m3 = 3000
    return volume_m3 * density_kg_per_m3

def calculate_ars(mass_kg, velocity_kms, hazardous):
    base_score = math.log10(mass_kg) * velocity_kms * 0.01
    if hazardous:
        base_score += 3
    return round(base_score, 1)

def get_risk_tier(ars):
    if ars >= 7:
        return "HIGH"
    elif ars >= 4:
        return "MODERATE"
    else:
        return "NEGLIGIBLE"

def fetch_spectral_type(designation):
    try:
        url = f"https://ssd-api.jpl.nasa.gov/sbdb.api?sstr={designation}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        spec = data.get("phys_par", {}).get("spec", None)
        return f"{spec}-type" if spec else "Unknown"
    except Exception as e:
        print(f"⚠️ Spectral lookup failed for {designation}: {e}")
        return "Unknown"

def mineral_mode(neo):
    designation = neo.get("neo_reference_id") or neo.get("name", "Unknown")
    spectral_type = fetch_spectral_type(designation)
    neo["composition"] = spectral_type
    neo["resource_flag"] = spectral_type.startswith("M")

def display_neo_alert(neo):
    name = neo['name']
    ars = neo['ars']
    tier = neo['tier']
    timestamp = neo['timestamp_local']
    hazardous = neo['is_potentially_hazardous_asteroid']
    composition = neo.get("composition", "Unknown")
    resource_flag = neo.get("resource_flag", False)

    tier_icon = {
        "HIGH": "🔥",
        "MODERATE": "⚠️",
        "NEGLIGIBLE": "🟢"
    }.get(tier, "❔")

    border = "=" * 40
    print(f"\n{border}")
    print(f"{tier_icon}  {name}".center(40))
    print(f"{border}")
    print(f"ARS Score:      {ars}")
    print(f"Risk Tier:      {tier}")
    print(f"Local Time:     {timestamp}")
    print(f"Hazard Status:  {'Hazardous' if hazardous else 'Non-Hazardous'}")
    print(f"Composition:    {composition}")
    if hazardous:
        print("\n🚨 LOOK OUT FOR THIS ONE! 🚨")
    if resource_flag:
        print("💰 Resource-rich target for future missions!")
    print(f"{border}")

    neo_path = f"data_logs/neo_alert_log_{datetime.now().strftime('%Y-%m-%d')}.json"
    mirror_data = {
        "name": neo.get("name"),
        "neo_reference_id": neo.get("neo_reference_id"),
        "ars": neo.get("ars"),
        "tier": neo.get("tier"),
        "timestamp_local": neo.get("timestamp_local"),
        "hazardous": neo.get("is_potentially_hazardous_asteroid"),
        "composition": neo.get("composition", "Unknown"),
        "resource_flag": neo.get("resource_flag", False)
    }

    file = Path(neo_path)
    if file.exists():
        with open(neo_path, "r") as f:
            log = json.load(f)
    else:
        log = []
    print("LOGGING:", mirror_data)
    print("SAVING TO:", os.path.abspath(neo_path))
    log.append(mirror_data)
import subprocess
from datetime import date

from datetime import date
import os

neo_path = os.path.join("data_logs", f"neo_alert_log_{date.today()}.json")

# Stage the file
subprocess.run(["git", "add", neo_path], check=True)

# Check if anything is staged
status = subprocess.run(["git", "diff", "--cached", "--quiet"])
if status.returncode != 0:
    # Changes ARE staged → commit & push
    subprocess.run(["git", "commit", "-m", f"Add NEO alert log for {date.today()}"], check=True)
    subprocess.run(["git", "push", "origin", "Solium-Core"], check=True)
    print("✅ Log file committed and pushed to GitHub.")
else:
    print("ℹ️ No changes staged—nothing to commit.")

# ---------- Main Execution ----------

if __name__ == "__main__":
    try:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        nasa_url = "https://api.nasa.gov/neo/rest/v1/feed"
        params = {
            "start_date": today,
            "end_date": today,
            "api_key": "DEMO_KEY"
        }

        response = requests.get(nasa_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        neos_today = data["near_earth_objects"][today]

        print("=" * 40)
        print(f"✅ {len(neos_today)} NEOs detected for {today} UTC:".center(40))
        print("=" * 40)

        for neo in neos_today:
            try:
                velocity = neo["close_approach_data"][0]["relative_velocity"]["kilometers_per_second"]
                velocity_kms = float(velocity)
                hazardous = neo["is_potentially_hazardous_asteroid"]
                diameter = neo["estimated_diameter"]["kilometers"]["estimated_diameter_max"]
                mass_kg = estimate_mass(diameter)

                close_time_str = neo["close_approach_data"][0]["close_approach_date_full"]
                close_time_utc = datetime.strptime(close_time_str, "%Y-%b-%d %H:%M")
                cdt = pytz.timezone("America/Chicago")
                local_time = close_time_utc.replace(tzinfo=pytz.utc).astimezone(cdt)
                local_timestamp = local_time.strftime("%Y-%m-%d %H:%M %Z")

                neo["ars"] = calculate_ars(mass_kg, velocity_kms, hazardous)
                neo["tier"] = get_risk_tier(neo["ars"])
                neo["timestamp_local"] = local_timestamp

                mineral_mode(neo)
                display_neo_alert(neo)
                mirror_to_json(neo)

            except Exception as err:
                print(f"⚠️ Skipping one NEO due to error: {err}")

    except Exception as e:
        print("⚠️ Critical failure while fetching or processing NEO data.")
        print(e)