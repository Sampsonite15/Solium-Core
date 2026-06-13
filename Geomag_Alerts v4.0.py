import requests

ALERTS_URL = "https://services.swpc.noaa.gov/products/alerts.json"

def fetch():
   try:
       r = requests.get(ALERTS_URL, timeout=10).json()

       border = "=" * 40
       print(f"\n{border}")
       print("🌐  GEOMAGNETIC ALERTS".center(40))
       print(f"{border}\n")

       for alert in reversed(r):
           msg = alert.get("message", "")
           print(msg)
           print("——————")

       print(f"{border}")

   except Exception as e:
       print(f"⚠️ Failed to fetch geomagnetic alerts: {e}")

if __name__ == "__main__":
   fetch()

