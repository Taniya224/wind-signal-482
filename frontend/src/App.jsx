
import { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import "./App.css";

const API = "";
function App() {
  const [data, setData] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      fetch(`${API}/api/wind`).then((r) => {
        if (!r.ok) throw new Error("Could not load wind data");
        return r.json();
      }),
      fetch(`${API}/api/metrics`).then((r) => {
        if (!r.ok) throw new Error("Could not load metrics");
        return r.json();
      }),
    ])
      .then(([windData, metricData]) => {
        setData(windData);
        setMetrics(metricData);
      })
      .catch(() => setError("Unable to connect to the backend. Check that FastAPI is running."));
  }, []);

  const chartData = data.map((item) => ({
    ...item,
    time: new Date(item.timestamp).toLocaleString("en-GB", {
      day: "2-digit",
      month: "short",
      hour: "2-digit",
      minute: "2-digit",
      timeZone: "Europe/London",
    }),
  }));

  return (
    <main className="dashboard">
      <header className="header">
        <div>
          <p className="eyebrow">ENERGY INTELLIGENCE</p>
          <h1>UK Wind Analytics</h1>
          <p className="subtitle">
            Wind generation forecast and actual performance · January 2026
          </p>
        </div>
        <span className="status">Historical data</span>
      </header>

      {error && <p className="error">{error}</p>}

      <section className="metrics">
        <article className="metric-card">
          <p>Matched hours</p>
          <h2>{metrics ? metrics.matched_hours : "—"}</h2>
          <span>January 2026</span>
        </article>
        <article className="metric-card">
          <p>Mean absolute error</p>
          <h2>
            {metrics
              ? `${metrics.mean_absolute_error_mw.toLocaleString()} MW`
              : "—"}
          </h2>
          <span>Average forecast error magnitude</span>
        </article>
        <article className="metric-card">
          <p>Mean forecast bias</p>
          <h2>
            {metrics
              ? `${metrics.mean_bias_mw > 0 ? "+" : ""}${metrics.mean_bias_mw.toLocaleString()} MW`
              : "—"}
          </h2>
          <span>Positive means forecasts were higher than actuals</span>
        </article>
      </section>

      <section className="panel">
        <div className="panel-heading">
          <div>
            <h2>Forecast vs actual generation</h2>
            <p>Hourly wind generation across January 2026</p>
          </div>
          <span className="unit">MW</span>
        </div>

        <div className="chart">
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="time"
                  interval={71}
                  tick={{ fontSize: 11 }}
                />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="forecast_mw"
                  name="Forecast"
                  stroke="#2563eb"
                  dot={false}
                  strokeWidth={2}
                />
                <Line
                  type="monotone"
                  dataKey="actual_mw"
                  name="Actual"
                  stroke="#0f9f78"
                  dot={false}
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <p className="loading">
              {error || "Loading wind generation data..."}
            </p>
          )}
        </div>
      </section>

      <section className="insight">
        <h2>Procurement insight</h2>
        <p>
          Wind forecasts help estimate how much renewable generation may be
          available. To estimate additional electricity procurement, the
          utility must also compare forecast wind generation with expected
          electricity demand and account for other available generation.
        </p>
        <p className="disclaimer">
          This dashboard compares wind forecasts with actual generation. It
          does not calculate a complete procurement requirement or use market
          prices.
        </p>
      </section>

      <footer>Data source: Elexon BMRS · FUELHH and WINDFOR</footer>
    </main>
  );
}

export default App;
