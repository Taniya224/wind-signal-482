
from elexon_client import fetch_actuals, fetch_forecasts

# Fetch a wider publication window so January delivery periods
# can include forecasts published during December.
start = "2025-12-01T00:00:00Z"
end = "2026-02-02T00:00:00Z"

actuals = fetch_actuals(start, end)
forecasts = fetch_forecasts(start, end)

print("\nTotal actual records:", len(actuals))
print("Total forecast records:", len(forecasts))

# Count records whose delivery start time falls in January.
january_actuals = [
    r for r in actuals
    if r["startTime"].startswith("2026-01-")
]

january_forecasts = [
    r for r in forecasts
    if r["startTime"].startswith("2026-01-")
]

print("\nJanuary actual records:", len(january_actuals))
print("January forecast records:", len(january_forecasts))

print("\nSample January actual:")
print(january_actuals[0] if january_actuals else "No records")

print("\nSample January forecast:")
print(january_forecasts[0] if january_forecasts else "No records")
