from collections import defaultdict, deque
from datetime import datetime, timedelta

# Rolling log buffer (per station)
ROLLING_WINDOW_HOURS = 24
buffer = defaultdict(lambda: deque(maxlen=ROLLING_WINDOW_HOURS * 60))  # 1 reading/minute

def log_reading(station, timestamp, H):
    buffer[station].append((timestamp, H))

def prune_old_data():
    cutoff = datetime.utcnow() - timedelta(hours=ROLLING_WINDOW_HOURS)
    for station in buffer:
        buffer[station] = deque(
            [(t, h) for t, h in buffer[station] if t >= cutoff],
            maxlen=ROLLING_WINDOW_HOURS * 60
        )
