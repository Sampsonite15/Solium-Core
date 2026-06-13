import requests
import base64
from datetime import datetime, timezone
from config import GITHUB_TOKEN

# ---------- Config ----------

GITHUB_USER = "Sampsonite15"
GITHUB_REPO = "Solium-Core"
BRANCH = "main"

API_BASE = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# ---------- Core Function ----------

def push_file(local_path, repo_path):
    try:
        with open(local_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"⚠️ File not found: {local_path}")
        return False

    encoded = base64.b64encode(content.encode()).decode()
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    url = f"{API_BASE}/{repo_path}"

    # Always fetch fresh SHA
    sha = None
    check = requests.get(url, headers=HEADERS, timeout=10)
    if check.status_code == 200:
        sha = check.json().get("sha")

    payload = {
        "message": f"Auto-update {repo_path} — {timestamp}",
        "content": encoded,
        "branch": BRANCH
    }
    if sha:
        payload["sha"] = sha

    response = requests.put(url, headers=HEADERS, json=payload, timeout=10)

    if response.status_code in (200, 201):
        action = "Updated" if sha else "Created"
        print(f"✅ {action}: {repo_path}")
        return True
    else:
        print(f"⚠️ Failed to push {repo_path}: {response.status_code} — {response.json().get('message')}")
        return False

def push_all():
    border = "=" * 40
    print(f"\n{border}")
    print("🐙  GITHUB AUTO-PUSH".center(40))
    print(f"{border}")

    files = [
        ("CENOS_Alerts v5.2.0.py", "CENOS_Alerts v5.2.0.py"),
        ("CENOS_mirror_json.py",   "CENOS_mirror_json.py"),
        ("mirror_to_json.py",      "mirror_to_json.py"),
        ("dedupe_cenos.py",        "dedupe_cenos.py"),
        ("pK_fetcher.py",          "pK_fetcher.py"),
        ("Kp Tracker.py",          "Kp Tracker.py"),
        ("Geomag_Alerts v4.0.py",  "Geomag_Alerts v4.0.py"),
        ("DeltaB Calculator.py",   "DeltaB Calculator.py"),
        ("DeltaB_Rolling_Log.py",  "DeltaB_Rolling_Log.py"),
        ("github_push.py",         "github_push.py"),
    ]

    success = 0
    for local, remote in files:
        if push_file(local, remote):
            success += 1

    print(f"\n✅ Pushed {success}/{len(files)} files to GitHub")
    print(f"{border}")

if __name__ == "__main__":
    push_all()
