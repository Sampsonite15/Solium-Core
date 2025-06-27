# 🛰️ CENOS_Alerts

Automated logging system for Near-Earth Objects (NEOs) based on NASA’s public API.  
Each version is archived in `/versions/`, with daily logs stored in `/data_logs/`.

## 📌 Version History
| Version | Description |
|---------|-------------|
| v3.0    | First release – basic logging only |
| v4.2    | Risk scoring introduced |
| v5.0 → 5.2.2 | Added ARS system, Git push, and logging refinements |
| v5.2.3  | 🚀 Modularized into `neo_logger.py`, `log_utils.py`, and `git_utils.py` |
| →       | Task Scheduler-ready, stable log formatting |

## 📁 Structure
```
CENOS_Alerts/ ├── data_logs/             # Daily NEO log output (auto-generated) ├── versions/              # Archived versions of the logger │   ├── v3.0/              # Initial release script │   ├── v4.2/              # Introduced basic risk scoring │   ├── v5.0/              # Refined output formatting │   ├── v5.0.1/            # Minor logging improvements │   ├── v5.1.1/            # Added ARS calculations │   ├── v5.2.0/            # Introduced hourly logging │   ├── v5.2.1/            # Integrated Git push automation │   ├── v5.2.2/            # Introduced modular design (pre-launch) │   └── v5.2.3/            # Stable, modular, fully scheduled version │       ├── neo_logger.py     # Main NEO ingestion + scoring script │       ├── log_utils.py      # Handles JSON logging logic │       └── git_utils.py      # Git automation for log pushing ├── .gitignore             # Excludes system files, pycache, etc. └── README.md              # Project overview, instructions, and version log

## ⚙️ Running the Logger
Schedule the logger (e.g. v5.2.3) daily via Windows Task Scheduler:
```

## 🛠️ Dependencies
- Python 3.x
- `requests`
- `pytz`

## 📡 Data Source
[NASA NeoWS API](https://api.nasa.gov/)

## ✍️ Author
Andy — Orbital pipeline engineer with attitude 😎