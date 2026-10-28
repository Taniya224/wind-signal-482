
import httpx

BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1"

params = {
    "publishDateTimeFrom": "2026-01-01T00:00:00Z",
    "publishDateTimeTo": "2026-01-02T00:00:00Z",
}

for dataset in ["FUELHH", "WINDFOR"]:
    print(f"\n--- {dataset} ---")

    url = f"{BASE_URL}/datasets/{dataset}/stream"

    try:
        response = httpx.get(url, params=params, timeout=30)
        print("Status:", response.status_code)
        response.raise_for_status()

        records = response.json()
        print("Records returned:", len(records))

        if dataset == "FUELHH":
            records = [
                r for r in records
                if r.get("fuelType") == "WIND"
            ]

        print("Relevant records:", len(records))

        for record in records[:5]:
            print(record)

    except Exception as error:
        print("Error:", error)
