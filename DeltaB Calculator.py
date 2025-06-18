from collections import defaultdict

def compute_deltaB(readings):
    """
    readings: list of dicts like:
    [
      {"station": "BOU", "timestamp": ..., "H": ..., "D": ..., "Z": ...},
      ...
    ]
    Returns:
        dict of {station: deltaB}, where deltaB is the absolute H change (nT)
    """
    deltas = defaultdict(list)

    # Group readings by station
    for reading in readings:
        deltas[reading["station"]].append(reading)

    deltaB_output = {}
    for station, station_data in deltas.items():
        station_data.sort(key=lambda x: x["timestamp"])

        if len(station_data) < 2:
            continue  # need at least 2 points to compute delta

        # Compute delta H as a proxy
        prev = station_data[-2]["H"]
        curr = station_data[-1]["H"]
        deltaH = abs(curr - prev)

        deltaB_output[station] = round(deltaH, 2)  # in nanotesla

    return deltaB_output
