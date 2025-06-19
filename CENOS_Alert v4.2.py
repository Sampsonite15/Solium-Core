import requests
import math
from datetime import datetime

# --- Configurations ---
nasa_url = "https://api.nasa.gov/neo/rest/v1/feed"
params = {
    "start_date": datetime.utcnow().strftime("%Y-%m-%d"),
    "end_date": datetime.utcnow().strftime("%Y-%m-%d"),
    "api_key": "DEMO_KEY"
}
today = datetime.utcnow().strftime("%Y-%m-%d")
MAX_DISPLAYED_NEOS = 10

# --- Helper Functions ---
def estimate_mass(diameter_km, density_kg_m3=3000):
    radius_m = (diameter_km * 1000) / 2
    volume_m3 = (4/3) * math.pi * (radius_m ** 3)
    return volume_m3 * density_kg_m3

mass_chicxulub = estimate_mass(12.5)
velocity_chicxulub = 20  # km/s
ke_chicxulub = 0.5 * mass_chicxulub * (velocity_chicxulub * 1000) ** 2

def calculate_ars(mass_kg, velocity_kms, hazardous):
    kinetic_energy = 0.5 * mass_kg * (velocity_kms * 1000) ** 2
    ratio = kinetic_energy / ke_chicxulub
    ars_base = math.log10(ratio * 1_000_000 + 1)
    hazard_multiplier = 1.2 if hazardous else 1.0
    return ars_base * hazard_multiplier

def get_risk_tier(ars):
    if ars >= 5:
        return "[SEVERE]"
    elif ars >= 2:
        return "[HIGH]"
    elif ars >= 0.5:
        return "[MODERATE]"
    elif ars >= 0.1:
        return "[LOW]"
    else:
        return "[NEGLIGIBLE]"

# --- Main Execution ---
if __name__ == '__main__':
    try:
        response = requests.get(nasa_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        neos_today = data["near_earth_objects"][today]
        print(f"✅ {len(neos_today)} NEOs detected today:\n")
    except requests.exceptions.RequestException as e:
        print(f"🚨 Network error while contacting NASA API: {e}")
        neos_today = []
    except (KeyError, ValueError) as e:
        print(f"⚠️ Data parsing error: {e}")
        neos_today = []

    for obj in neos_today[:MAX_DISPLAYED_NEOS]:
        try:
            diameter_km = float(obj['estimated_diameter']['kilometers']['estimated_diameter_max'])
            velocity_kms = float(obj['close_approach_data'][0]['relative_velocity']['kilometers_per_second'])
            hazardous = obj['is_potentially_hazardous_asteroid']
            mass_kg = estimate_mass(diameter_km)

            ars = calculate_ars(mass_kg, velocity_kms, hazardous)
            tier = get_risk_tier(ars)

            try:
                print(f"DEBUG: ARS = {ars:.2f}, Tier = {tier}")
            except Exception as e:
                print(f"⚠️ Debug print failed: {e}")

            print(f"{obj['name']} | ARS: {ars:.2f} / 10 | Tier: {tier} | Hazardous: {hazardous}")
        except (KeyError, IndexError, ValueError) as e:
            print(f"⚠️ Skipped object due to data issue: {e}")