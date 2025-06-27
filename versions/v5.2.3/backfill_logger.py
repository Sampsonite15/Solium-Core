# backfill_logger.py

import subprocess
from datetime import datetime, timedelta
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Run CENOS_Alerts logger across a date range.")
    parser.add_argument("--start", required=True, help="Start date in YYYY-MM-DD format")
    parser.add_argument("--end", required=True, help="End date in YYYY-MM-DD format")
    return parser.parse_args()


def date_range(start_date, end_date):
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days=1)


def main():
    args = parse_args()
    start = datetime.strptime(args.start, "%Y-%m-%d").date()
    end = datetime.strptime(args.end, "%Y-%m-%d").date()

    print(f"🚀 Backfilling logs from {start} to {end}")

    for log_date in date_range(start, end):
        print(f"\n📅 Fetching NEOs for: {log_date}")
        subprocess.run([
            "python",
            "neo_logger.py",
            "--date",
            log_date.isoformat()
        ])


if __name__ == "__main__":
    main()