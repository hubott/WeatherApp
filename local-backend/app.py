import requests
import os
from dotenv import load_dotenv
import json
import datetime

load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')
cityName = "Melbourne"
Coords_URL = f"http://api.openweathermap.org/geo/1.0/direct?q={cityName}&appid={API_KEY}"
coordReponse = requests.get(Coords_URL).json()
lat = coordReponse[0]['lat']
lon = coordReponse[0]['lon']
URL = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'

fetched_at = datetime.datetime.now(datetime.timezone.utc)

response = requests.get(URL).json()


payload = {
    "fetched_at": fetched_at.isoformat(),
    "data": response
}
with open("sample_response.json", "w") as f:
    json.dump(payload, f, indent=4)
