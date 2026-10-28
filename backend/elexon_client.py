
from datetime import datetime, timedelta, timezone

import httpx

BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1"


def fetch_dataset(dataset, start, end):
    """Fetch records in daily publication-time windows."""
    records = []

    current = datetime.fromisoformat(
        start.replace("Z", "+00:00")
    )
    end_time = datetime.fromisoformat(
        end.replace("Z", "+00:00")
    )

    with httpx.Client(timeout=60) as client:
        while current < end_time:
            next_time = min(
                current + timedelta(days=1),
                end_time,
            )

            params = {
                "publishDateTimeFrom": current.isoformat(),
                "publishDateTimeTo": next_time.isoformat(),
            }

            url = f"{BASE_URL}/datasets/{dataset}/stream"

            response = client.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            if isinstance(data, dict):
                data = data.get("data", [])

            records.extend(data)

            print(
                f"{dataset}: {current.date()} "
                f"returned {len(data)} records"
            )

            current = next_time

    return records


def fetch_actuals(start, end):
    records = fetch_dataset("FUELHH", start, end)

    return [
        record for record in records
        if record.get("fuelType") == "WIND"
        and record.get("startTime")
    ]


def fetch_forecasts(start, end):
    records = fetch_dataset("WINDFOR", start, end)

    return [
        record for record in records
        if record.get("startTime")
        and record.get("publishTime")
        and record.get("generation") is not None
    ]
