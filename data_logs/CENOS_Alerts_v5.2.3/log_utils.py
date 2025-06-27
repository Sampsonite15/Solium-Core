# log_utils.py
import os
import json

def ensure_directory_exists(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def load_log(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_log_entry(path, new_entry):
    ensure_directory_exists(path)
    log = load_log(path)
    log.append(new_entry)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)
    print(f"✅ Saved log entry to {path}")