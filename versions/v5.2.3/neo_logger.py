import argparse
import os
import json

def parse_args():
    parser = argparse.ArgumentParser(description="Log NEO data for a specific date.")
    parser.add_argument("--date", required=True, help="Date in YYYY-MM-DD format")
    return parser.parse_args()

def save_neo_log(target_date):
    # Create the log directory if it doesn't exist
    log_dir = "data_logs"
    os.makedirs(log_dir, exist_ok=True)

    # Build the filename using the target date
    filename = os.path.join(log_dir, f"neo_alert_log_{target_date}.json")

    # Example NEO data (replace with real data fetching logic)
    neo_data = {
        "date": target_date,
        "neos": [
            {"name": "Asteroid 2025 AB", "diameter_km": 0.15},
            {"name": "Asteroid 2025 XY", "diameter_km": 0.42}
        ]
    }

    # Save the data to a JSON file
    with open(filename, "w") as f:
        json.dump(neo_data, f, indent=4)

    print(f"✅ Saved NEO log to {filename}")

def main():
    args = parse_args()
    save_neo_log(args.date)

if __name__ == "__main__":
    main()