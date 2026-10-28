# UK Wind Analytics Dashboard

A full-stack analytics dashboard for comparing forecasted and actual UK wind power generation during January 2026. The application helps an energy utility understand wind forecast errors and evaluate their implications for electricity procurement planning.

## Live Demo

- **Frontend:** https://wind-signal-dashboard-3e6wdqioq-mine-be27.vercel.app
- **Backend API:** https://wind-signal-482.onrender.com
- **API Metrics:** https://wind-signal-482.onrender.com/api/metrics
- **API Wind Data:** https://wind-signal-482.onrender.com/api/wind

## Features

- Compares forecasted and actual wind generation.
- Displays forecast error metrics, including mean absolute error (MAE) and mean bias.
- Visualizes forecast-versus-actual generation over time.
- Uses January 2026 data from the Elexon BMRS API.
- Provides insights to support electricity procurement planning.

## Technology Stack

- **Frontend:** React, Vite, Recharts
- **Backend:** Python, FastAPI, Pandas, HTTPX
- **Containerization:** Docker
- **Deployment:** Vercel (frontend), Render (backend)
- **Data source:** Elexon BMRS API

## Project Structure

```text
wind-signal-482/
├── backend/
│   ├── main.py
│   ├── elexon_client.py
│   ├── processing.py
│   ├── january_wind_data.csv
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Running Locally

### Prerequisites

Install Python, Node.js, and Git. Docker is optional.

### 1. Start the backend

Open a terminal in the project root:

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies and start the API:

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The backend will run at `http://127.0.0.1:8000`.

### 2. Start the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite in your terminal.

For local development, configure the frontend API URL and Vite proxy as appropriate for your backend port.

## API Endpoints

- `GET /` — API status.
- `GET /api/wind` — Hourly wind forecast and actual generation data.
- `GET /api/metrics` — Summary forecast accuracy metrics.

## Data Processing and Assumptions

The application processes Elexon wind generation actuals and forecasts for January 2026. Half-hourly actual generation observations are aggregated into hourly values. Forecasts are matched with the corresponding delivery hours, using the latest forecast published before the selected procurement cutoff.

The implementation uses a 09:45 UTC forecast cutoff as a working assumption. This should not be interpreted as a confirmed official market deadline. Forecast errors are calculated as forecast generation minus actual generation.

Mean absolute error measures the average magnitude of forecast errors. Mean bias indicates whether forecasts tend to be higher or lower than actual generation.

Forecast accuracy alone does not determine procurement requirements. Electricity demand, other generation sources, market prices, and operational constraints must also be considered.

## Deployment

- Frontend hosted on Vercel.
- Backend hosted on Render.
- Backend containerized using Docker.

## AI Tools Disclosure

ChatGPT was used to support project planning, implementation guidance, debugging, and documentation. The application was tested locally and deployed to public hosting services.

## Limitations and Future Improvements

- Incorporate electricity demand forecasts and other generation sources.
- Add market-price data to estimate procurement costs.
- Improve forecast evaluation across different time periods.
- Add interactive date filters and downloadable reports.
- Validate procurement cutoff assumptions against official market rules.

