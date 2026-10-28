
from pathlib import Path

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="UK Wind Analytics API")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = Path(__file__).parent / "january_wind_data.csv"


def load_data():
    if not DATA_FILE.exists():
        return pd.DataFrame()

    data = pd.read_csv(DATA_FILE)
    data["timestamp"] = pd.to_datetime(data["timestamp"], utc=True)
    return data


@app.get("/")
def home():
    return {"message": "UK Wind Analytics API is running"}


@app.get("/api/wind")
def get_wind_data():
    data = load_data()

    if data.empty:
        return []

    data["timestamp"] = data["timestamp"].dt.strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    return data.to_dict(orient="records")


@app.get("/api/metrics")
def get_metrics():
    data = load_data()

    if data.empty:
        return {"error": "No processed data available"}

    return {
        "matched_hours": len(data),
        "mean_absolute_error_mw": round(
            data["absolute_error_mw"].mean(), 2
        ),
        "mean_bias_mw": round(data["error_mw"].mean(), 2),
    }
