import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

function HourlyGraph({ data }) {
  if (!data || data.length === 0) return null;

  return (
    <LineChart width={800} height={300} data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
      <XAxis 
        dataKey="forecast_time" 
        tickFormatter={t => new Date(t).getHours() + ":00"} 
      />
      <YAxis />
      <Tooltip labelFormatter={t => new Date(t).toLocaleString()} />
      <CartesianGrid stroke="#eee" strokeDasharray="5 5"/>
      <Line type="monotone" dataKey="temperature" stroke="#8884d8" />
      <Line type="monotone" dataKey="feels_like" stroke="#82ca9d" />
    </LineChart>
  );
}

export default HourlyGraph;
