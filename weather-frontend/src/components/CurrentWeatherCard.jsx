import React from "react";
import "../style.css";

function CurrentWeatherCard({ weather }) {
  
  if (!weather) return null;
  //Set the url for the icon, provided by OpenWeatherMap
  const iconUrl = `https://openweathermap.org/img/wn/${weather.icon}@2x.png`;

  return (

        <div className="current">
        <div className="icon-wrap">
            
            <img src={iconUrl} alt={weather.weather} width="56" height="56" />
        </div>
        <div>
            <div className="temp">{weather.temperature.toFixed(1)}°C</div>
            <div className="meta">Feels like {weather.feels_like.toFixed(1)}°C</div>
        </div>
        <div className="stats">
            <div className="stat"><div className="label">Humidity</div><div className="value">{weather.humidity}%</div></div>
            <div className="stat"><div className="label">Condition</div><div className="value">{weather.weather}</div></div>
        </div>
        </div>
    
  );
}

export default CurrentWeatherCard;
