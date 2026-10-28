
from collections import Counter
from elexon_client import fetch_actuals, fetch_forecasts

start = "2025-12-01T00:00:00Z"
end = "2026-02-02T00:00:00Z"

actuals = fetch_actuals(start, end)
forecasts = fetch_forecasts(start, end)

for name, records in [
    ("ACTUALS", actuals),
    ("FORECASTS", forecasts),
]:
    print("\n---", name, "---")
    print("Total records:", len(records))

    publish_times = [
        r["publishTime"] for r in records
        if r.get("publishTime")
    ]
    start_times = [
        r["startTime"] for r in records
        if r.get("startTime")
    ]

    print("Distinct publication times:", len(set(publish_times)))
    print("Earliest publication:", min(publish_times, default="None"))
    print("Latest publication:", max(publish_times, default="None"))
    print("Earliest delivery:", min(start_times, default="None"))
    print("Latest delivery:", max(start_times, default="None"))

    keys = [
        (r.get("publishTime"), r.get("startTime"), r.get("generation"))
        for r in records
    ]
    print("Duplicate time/value combinations:",
          len(keys) - len(set(keys)))

    print("Example record keys:",
          list(records[0].keys()) if records else "No records")
