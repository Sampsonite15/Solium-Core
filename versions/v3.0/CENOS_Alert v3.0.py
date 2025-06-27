import requests
import json
import math
from datetime import date

MAX_DISPLAYED_NEOS = 20

# 📅 Use today's date
today = date.today().isoformat()
api_key = "DEMO_KEY"  # Replace with your NASA key if you have one

nasa_url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={today}&api_key={api_key}"

def calculate_ars(estimated_diameter_m):
    radius = estimated_diameter_m / 2
    volume = (4/3) * math.pi * radius**3
    density = 3000  # kg/m³ for rocky asteroid
    mass = volume * density  # in kilograms

    # Normalize and bias toward size
    mass_score = max(math.log10(mass) - 10, 0)   # Normalize from 0+
    size_score = estimated_diameter_m / 100      # Normalize 100m = 1

    ars = 0.4 * mass_score + 0.6 * size_score
    return round(min(ars, 10), 2)

try:
    print(f"🔭 Contacting NASA for NEO data on {today}...")
    response = requests.get(nasa_url, timeout=10)
    response.raise_for_status()

    data = response.json()
    neos_today = data["near_earth_objects"][today]
    print(f"✅ {len(neos_today)} NEOs detected today:\n")

    for obj in neos_today[:MAX_DISPLAYED_NEOS]:  # Limit for display
        name = obj["name"]
        approach = obj["close_approach_data"][0]
        distance_km = float(approach["miss_distance"]["kilometers"])
        velocity_kms = float(approach["relative_velocity"]["kilometers_per_second"])
        hazardous = obj["is_potentially_hazardous_asteroid"]

        # Diameter estimate
        d_min = obj["estimated_diameter"]["meters"]["estimated_diameter_min"]
        d_max = obj["estimated_diameter"]["meters"]["estimated_diameter_max"]
        diameter_m = (d_min + d_max) / 2

        ars = calculate_ars(diameter_m)
        status = "⚠️ HAZARDOUS" if hazardous else "✅ Not hazardous"

        print(f"🛰️ {name}")
        print(f"   → Distance: {distance_km:,.0f} km")
        print(f"   → Speed: {velocity_kms:.2f} km/s")
        print(f"   → Diameter: {diameter_m:.1f} m")
        print(f"   → Risk Score (ARS): {ars}/10")
        print(f"   → Status: {status}\n")

except requests.exceptions.SSLError:
    print("❌ SSL error—NASA endpoint not trusted.")
except Exception as e:
    print("❌ Request failed:", e)