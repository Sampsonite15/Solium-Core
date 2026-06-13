import requests
import datetime
import pytz

def fetch_kp_index():
    url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        latest = data[-1]
        timestamp_utc = latest["time_tag"]
        kp_value = latest["Kp"]

        utc_time = datetime.datetime.fromisoformat(timestamp_utc)
        cdt = pytz.timezone("America/Chicago")
        cdt_time = utc_time.replace(tzinfo=pytz.utc).astimezone(cdt)

        print(f"Kp Index as of {cdt_time.strftime('%Y-%m-%d %I:%M %p %Z')}: {kp_value}")

    except Exception as e:
        print(f"Error retrieving Kp index: {e}")

if __name__ == "__main__":
    fetch_kp_index()
