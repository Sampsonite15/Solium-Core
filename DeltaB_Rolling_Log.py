from datetime import datetime, timedelta

# Store recent readings
log = []

ROLLING_WINDOW_MINUTES = 30

def log_reading(station, timestamp, h_value):
    entry = {
        "station": station,
        "timestamp": timestamp,
        "H": h_value
    }
    log.append(entry)
    print(f"📝 Logged reading: {station} @ {timestamp} → H = {h_value}")

def prune_old_data():
    global log
    cutoff = datetime.utcnow() - timedelta(minutes=ROLLING_WINDOW_MINUTES)
    pruned_log = []

    for entry in log:
        try:
            timestamp = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
            if timestamp >= cutoff:
                pruned_log.append(entry)
        except Exception as e:
            print(f"⚠️ Timestamp parse error: {entry.get('timestamp')} → {e}")

    print(f"🧹 Pruned log: {len(log)} → {len(pruned_log)} entries")
    log = pruned_log

def get_log():
    return log.copy()