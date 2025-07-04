# backfill_logger.py

import subprocess
from datetime import datetime, timedelta
import argparse
from datetime import datetime
import os
import json

def date_range(start_date, end_date):
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days=1)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", required=False)
    parser.add_argument("--end", required=False)
    args = parser.parse_args()

    if not args.start or not args.end:
        print("⚠️ No arguments provided. Using default range.")
        args.start = "2025-06-21"
        args.end = "2025-07-03"

    return args

def main():
    args = parse_args()
    start = datetime.strptime(args.start, "%Y-%m-%d").date()
    end = datetime.strptime(args.end, "%Y-%m-%d").date()

    print(f"🚀 Backfilling logs from {start} to {end}")

    for log_date in date_range(start, end):
        date_str = log_date.strftime("%Y-%m-%d")
        print(f"\n🛰️ Fetching NEOs for: {date_str}")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        neo_logger_path = os.path.join(script_dir, "neo_logger.py")

        subprocess.run(["python", neo_logger_path, "--date", date_str])

if __name__ == "__main__":
    main()