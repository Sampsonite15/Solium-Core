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

## ⚙️ Running the Logger
Schedule the logger (e.g. v5.2.3) daily via Windows Task Scheduler:


## 🛠️ Dependencies
- Python 3.x
- `requests`
- `pytz`

## 📡 Data Source
[NASA NeoWS API](https://api.nasa.gov/)

## ✍️ Author
Andy — Orbital pipeline engineer with attitude 😎