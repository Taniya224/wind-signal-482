
import pandas as pd

from elexon_client import fetch_actuals, fetch_forecasts


def build_january_dataset():
    start = "2025-12-01T00:00:00Z"
    end = "2026-02-02T00:00:00Z"

    actuals = fetch_actuals(start, end)
    forecasts = fetch_forecasts(start, end)

    # Prepare actual generation data.
    actual_df = pd.DataFrame(actuals)
    actual_df["startTime"] = pd.to_datetime(
        actual_df["startTime"], utc=True
    )
    actual_df["publishTime"] = pd.to_datetime(
        actual_df["publishTime"], utc=True
    )

    # Keep the latest published version of each half-hour period.
    actual_df = actual_df.sort_values("publishTime")
    actual_df = actual_df.drop_duplicates(
        subset=["startTime"], keep="last"
    )

    # Keep January delivery periods only.
    actual_df = actual_df[
        (actual_df["startTime"] >= "2026-01-01")
        & (actual_df["startTime"] < "2026-02-01")
    ].copy()

    # Convert half-hourly actuals into hourly averages.
    actual_df["hour"] = actual_df["startTime"].dt.floor("h")

    hourly_actuals = (
        actual_df.groupby("hour")["generation"]
        .mean()
        .reset_index()
    )

    hourly_actuals = hourly_actuals.rename(
        columns={"hour": "timestamp", "generation": "actual_mw"}
    )

    # Prepare forecast data.
    forecast_df = pd.DataFrame(forecasts)
    forecast_df["startTime"] = pd.to_datetime(
        forecast_df["startTime"], utc=True
    )
    forecast_df["publishTime"] = pd.to_datetime(
        forecast_df["publishTime"], utc=True
    )

    forecast_df = forecast_df[
        (forecast_df["startTime"] >= "2026-01-01")
        & (forecast_df["startTime"] < "2026-02-01")
    ].copy()

    # Decision cutoff: 09:00 UTC on the day before delivery.
    forecast_df["cutoff"] = (
        forecast_df["startTime"].dt.normalize()
        - pd.Timedelta(days=1)
        + pd.Timedelta(hours=9, minutes=45)
    )

    forecast_df = forecast_df[
        forecast_df["publishTime"] <= forecast_df["cutoff"]
    ]

    # Select the latest eligible forecast for each delivery hour.
    forecast_df = forecast_df.sort_values("publishTime")
    forecast_df = forecast_df.drop_duplicates(
        subset=["startTime"], keep="last"
    )

    hourly_forecasts = forecast_df[
        ["startTime", "generation"]
    ].rename(
        columns={
            "startTime": "timestamp",
            "generation": "forecast_mw",
        }
    )

    # Compare forecasts with actual generation.
    result = pd.merge(
        hourly_forecasts,
        hourly_actuals,
        on="timestamp",
        how="inner",
    )

    result = result.sort_values("timestamp")
    result["error_mw"] = result["forecast_mw"] - result["actual_mw"]
    result["absolute_error_mw"] = result["error_mw"].abs()

    return result


if __name__ == "__main__":
    data = build_january_dataset()
    data.to_csv("january_wind_data.csv", index=False)
    print("\nSaved data to january_wind_data.csv")

    print("\nMatched hourly records:", len(data))
    print("\nFirst five rows:")
    print(data.head().to_string(index=False))

    if not data.empty:
        print("\nMean absolute error (MW):",
              round(data["absolute_error_mw"].mean(), 2))
        print("Mean error / bias (MW):",
              round(data["error_mw"].mean(), 2))
    else:
        print("No matching forecast and actual records found.")
