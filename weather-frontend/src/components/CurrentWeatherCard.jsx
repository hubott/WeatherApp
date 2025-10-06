import React from "react";
import "../style.css";

function CurrentWeatherCard({ weather }) {
  const bgColors = {
  "01d": "#118ef5ff", // clear day
  "02d": "#6aa4caff", // few clouds day
  "03d": "#7e91a7ff", // scattered clouds day
  "04d": "#7381a1ff", // broken clouds day
  "09d": "#9fb0cbff", // rain
  "10d": "#8ca8c8ff", // rain day
  "11d": "#6b7388ff", // thunderstorm
  "13d": "#b3c6eaff", // snow
  "50d": "#dfe6f4ff", // mist
  "01n": "#7c839aff", // clear night
  "02n": "#4a5a7aff", // few clouds night
  "03n": "#455363ff", // scattered clouds night
  "04n": "#5b5f68ff", // broken clouds night
  "09n": "#5a6b8aff", // rain night
  "10n": "#63728cff", // rain night
  "11n": "#0f1012ff", // thunderstorm night
  "13n": "#6b7388ff", // snow night
  "50n": "#9aa0b9ff", // mist night

  // … add more as needed
  
};
  
  if (!weather) return null;
  //Set the url for the icon, provided by OpenWeatherMap
  const iconUrl = `https://openweathermap.org/img/wn/${weather.icon}@2x.png`;

  return (

        <div className="current">
        <div className="icon-wrap"
        style={{background: bgColors[weather.icon] || '#f5fbe0ff'}}>
            
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
