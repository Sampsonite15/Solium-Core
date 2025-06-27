# neo_logger.py
from datetime import datetime, timedelta
import pytz
import requests
from log_utils import save_log_entry
from git_utils import push_log_to_git

__version__ = "5.2.3"

log_start_date = "2025-06-27"  # Official launch

CENTRAL = pytz.timezone("America/Chicago")
now_kansas = datetime.now(CENTRAL)
today_str = now_kansas.strftime("%Y-%m-%d")
log_path = f"data_logs/neo_alert_log_{today_str}.json"

def estimate_mass(diameter_km):
    r_m = (diameter_km * 1000) / 2
    vol = (4 / 3) * 3.1416 * r_m**3
    return vol * 3000

def calculate_ars(mass_kg, velocity_kms, hazardous):
    base = (mass_kg**0.5) * velocity_kms * 0.005
    return round(base + (3 if hazardous else 0), 1)

def get_risk_tier(ars):
    return "HIGH" if ars >= 7 else "MODERATE" if ars >= 4 else "NEGLIGIBLE"

def mirror_to_json(neo):
    return {
        "name": neo.get("name"),
        "neo_reference_id": neo.get("neo_reference_id"),
        "ars": neo.get("ars"),
        "tier": neo.get("tier"),
        "timestamp_local": neo.get("timestamp_local"),
        "hazardous": neo.get("is_potentially_hazardous_asteroid"),
        "composition": neo.get("composition", "Unknown"),
        "resource_flag": neo.get("resource_flag", False)
    }

def run_cenos_logger():
    nasa_url = "https://api.nasa.gov/neo/rest/v1/feed"
    today = datetime.utcnow().strftime("%Y-%m-%d")
    params = {
        "start_date": today,
        "end_date": today,
        "api_key": "DEMO_KEY"
    }

    try:
        response = requests.get(nasa_url, params=params, timeout=10)
        response.raise_for_status()
        neos_today = response.json()["near_earth_objects"][today]

        print(f"\n🛰️ {len(neos_today)} NEOs detected for {today}")
        for neo in neos_today:
            try:
                velocity_kms = float(neo["close_approach_data"][0]["relative_velocity"]["kilometers_per_second"])
                diameter_km = neo["estimated_diameter"]["kilometers"]["estimated_diameter_max"]
                mass_kg = estimate_mass(diameter_km)
                hazardous = neo["is_potentially_hazardous_asteroid"]

                ars = calculate_ars(mass_kg, velocity_kms, hazardous)
                tier = get_risk_tier(ars)

                time_str = neo["close_approach_data"][0]["close_approach_date_full"]
                close_utc = datetime.strptime(time_str, "%Y-%b-%d %H:%M").replace(tzinfo=pytz.utc)
                local_time = close_utc.astimezone(CENTRAL).strftime("%Y-%m-%d %H:%M %Z")

                neo["ars"] = ars
                neo["tier"] = tier
                neo["timestamp_local"] = local_time
                neo["composition"] = "Unknown"  # Stubbed for v5.2.3
                neo["resource_flag"] = False

                entry = mirror_to_json(neo)
                save_log_entry(log_path, entry)

            except Exception as e:
                print(f"⚠️ Skipped one NEO due to error: {e}")

        push_log_to_git(log_path, f"🛰️ Added log for {today_str}")

    except Exception as e:
        print("🚫 Failed to fetch or process NEOs:", e)

if __name__ == "__main__":
    print(f"CENOS_Alerts v{__version__} starting for {today_str}")
    if today_str >= log_start_date:
        run_cenos_logger()
    else:
        print("🕒 Not logging before launch date.")