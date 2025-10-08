import axios from "axios";

const API_BASE = "http://weatherapp-env.eba-kfmvwpd7.ap-southeast-2.elasticbeanstalk.com/api";

export const fetchHourlyWeather = async (city="Melbourne") => {
  try {
    const res = await axios.get(`${API_BASE}/hourly?city=${city}`);
    console.log(res.data);
    return res.data;
  } catch (err) {
    console.error("Error fetching hourly weather:", err);
    return [];
  }
};
