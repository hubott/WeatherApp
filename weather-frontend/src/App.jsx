import React, { useState, useEffect } from "react";
import { fetchHourlyWeather } from "./api";
import CurrentWeatherCard from "./components/CurrentWeatherCard";
import HourlyGraph from "./components/HourlyGraph";
import "./style.css";

function App() {
  const [hourlyData, setHourlyData] = useState([]);
  const [lastRefreshed, setLastRefreshed] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const data = await fetchHourlyWeather();
      setHourlyData(data.hourly);
      setLastRefreshed(data.last_refreshed);
    };

    fetchData();
    const interval = setInterval(fetchData, 60 * 60 * 1000); // refresh every hour

    return () => clearInterval(interval);
  }, []);

  const currentWeather = hourlyData.length > 0 ? hourlyData[0] : null;

  return (
    <div className="container">
      <header className="app-header">
        <h1 className="app-title">Melbourne Weather Dashboard</h1>
        <div className="last-updated">Last updated: {new Date(lastRefreshed).toLocaleString()}</div>
      </header>
      <section className="card">
        <CurrentWeatherCard weather={currentWeather} />
      </section>
      <section className="card hourly">
      <h2 >Next 48 Hours</h2>
      <div className="chart">
        <HourlyGraph data={hourlyData} />
      </div>
      </section>
    </div>
  );
}

export default App;
