
import requests
import datetime

def fetch_kp_index():
    url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # The last element contains the most recent reading
        latest = data[-1]
        timestamp_utc = latest[0]
        kp_value = latest[1]

        # Convert timestamp to CDT
        utc_time = datetime.datetime.strptime(timestamp_utc, "%Y-%m-%d %H:%M:%S")
        cdt_time = utc_time - datetime.timedelta(hours=5)

        print(f"Kp Index as of {cdt_time.strftime('%Y-%m-%d %I:%M %p CDT')}: {kp_value}")
    except Exception as e:
        print(f"Error retrieving Kp index: {e}")

if __name__ == "__main__":
    fetch_kp_index()