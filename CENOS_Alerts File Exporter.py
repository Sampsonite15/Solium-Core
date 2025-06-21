import json
from datetime import datetime
import os

import datetime
today = datetime.date.today().strftime("%Y-%m-%d")
filepath = f"data_logs/neo_alert_log_{today}.json"

import os
os.makedirs("data_logs", exist_ok=True)

export_payload = {
    "timestamp": str(datetime.datetime.now()),
    "source": "CENOS_Alerts Exporter"
}
def export_daily_neo_log(data, export_dir="logs"):
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"neo_alert_log_{today}.json"
    os.makedirs(export_dir, exist_ok=True)

    export_payload = {
        "export_timestamp": datetime.now().isoformat(),
        "neo_data": data
    }

    filepath = os.path.join(export_dir, filename)


print("Exporter starting...")
try:
    with open(filepath, "w") as f:
        export_payload["export_status"] = "success"
        json.dump(export_payload, f, indent=4)
    print(f"[✔] Successfully exported log to {filepath}")
except Exception as e:
    export_payload = {}
    export_payload["export_status"] = "failure"
    export_payload["error_message"] = str(e)
    with open(filepath, "w") as f:
        json.dump(export_payload, f, indent=4)
    print(f"[✖] Export failed: {e}")
print("Exporter finished.")
