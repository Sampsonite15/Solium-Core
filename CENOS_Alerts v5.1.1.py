import requests
import math
from datetime import datetime
import pytz

# ---------- Core Functions ----------

def estimate_mass(diameter_km):
    radius_m = (diameter_km * 1000) / 2
    volume_m3 = (4/3) * math.pi * (radius_m ** 3)
    density_kg_per_m3 = 3000  # estimated rocky asteroid density
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

def mineral_mode(neo):
    """
    Assigns basic composition and resource flag based on designation.
    In the future, replace this with a real API or spectral database.
    """
    designation = neo.get("neo_reference_id") or neo.get("name", "Unknown")
    known_m_types = {"2001 FO32", "1986 DA", "16 Psyche", "468005"}

    if designation in known_m_types:
        neo["composition"] = "Metallic (M-type)"
        neo["resource_flag"] = True
    else:
        neo["composition"] = "Unknown"
        neo["resource_flag"] = False

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
        print(f"\n🚨 LOOK OUT FOR THIS ONE! 🚨")
    if resource_flag:
        print(f"💰 Resource-rich target for future missions!")

    print(f"{border}")

# ---------- Main Execution ----------

if __name__ == "__main__":
    try:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        nasa_url = "https://api.nasa.gov/neo/rest/v1/feed"
        params = {
            "start_date": today,
            "end_date": today,
            "api_key": "DEMO_KEY"  # Replace with your API key
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

                # Timestamp formatting to CDT
                close_time_str = neo["close_approach_data"][0]["close_approach_date_full"]
                close_time_utc = datetime.strptime(close_time_str, "%Y-%b-%d %H:%M")
                cdt = pytz.timezone("America/Chicago")
                local_time = close_time_utc.replace(tzinfo=pytz.utc).astimezone(cdt)
                local_timestamp = local_time.strftime("%Y-%m-%d %H:%M %Z")

                # Core calculations and flags
                neo["ars"] = calculate_ars(mass_kg, velocity_kms, hazardous)
                neo["tier"] = get_risk_tier(neo["ars"])
                neo["timestamp_local"] = local_timestamp

                # Bonus: Mineral Mode
                mineral_mode(neo)

                display_neo_alert(neo)

            except Exception as err:
                print(f"⚠️ Skipping one NEO due to error: {err}")

    except Exception as e:
        print("⚠️ Critical failure while fetching or processing NEO data.")
        print(e)