import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, Label } from "recharts";
import "../style.css";

function HourlyGraph({ data }) {
    const [graphType, setGraphType] = React.useState("temperature");
  if (!data || data.length === 0) return null;



  const yAxisLabel = {
    temperature: "Temperature (°C)",
    humidity: "Humidity (%)",
    pressure: "Pressure (hPa)",
    wind_speed: "Wind Speed (m/s)",
    clouds: "Cloudiness (%)",
    UVI: "UV Index"
  }[graphType];

const renderLines = () => {

    switch (graphType) {
      case "temperature":
        return (
          <>
            <Line type="monotone" dataKey="temperature" stroke="#8884d8" name="Temperature (°C)" />
            <Line type="monotone" dataKey="feels_like" stroke="#82ca9d" name="Feels Like (°C)" />
          </>
        );
      case "humidity":
        return <Line type="monotone" dataKey="humidity" stroke="#00bcd4" name="Humidity (%)" />;
      case "clouds":
        return <Line type="monotone" dataKey="clouds" stroke="#ff9800" name="Cloud Cover (%)" />;
      case "UVI":
        return <Line type="monotone" dataKey="UVI" stroke="#ff5722" name="UV Index" />;
      case "wind_speed":
        return <Line type="monotone" dataKey="wind_speed" stroke="#4caf50" name="Wind Speed (m/s)" />;
      default:
        return null;
    }
  };





  return (

    <div>
      <div className="graph-controls">
        <label htmlFor="graphType">Graph Type: </label>
        <select
          id="graphType"
          value={graphType}
          onChange={(e) => setGraphType(e.target.value)}
        >
          <option value="temperature">Temperature</option>
          <option value="humidity">Humidity</option>
            <option value="clouds">Cloud Cover</option>
            <option value="UVI">UV Index</option>
            <option value="wind_speed">Wind Speed</option>
        </select>
      </div>


    <LineChart width={800} height={300} data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
      <XAxis 
        dataKey="forecast_time" 
        tickFormatter={t => new Date(t).getHours() + ":00"} 
      />
      <YAxis>
        <Label
            value={yAxisLabel}
            angle={-90}
            position="insideLeft"
            style={{ textAnchor: "middle" }}
          />
      </YAxis>

      <Tooltip labelFormatter={t => new Date(t).toLocaleString()} />
      <CartesianGrid stroke="#eee" strokeDasharray="5 5"/>
      {renderLines()}
    </LineChart>
    </div>
  );
}

export default HourlyGraph;
