import requests
import os
from dotenv import load_dotenv
import json
import datetime

load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')
melbourne_lat = 37.81
melbourne_lon = 144.96
URL = f'https://api.openweathermap.org/data/3.0/onecall?lat={melbourne_lat}&lon={melbourne_lon}&appid={API_KEY}'

fetched_at = datetime.datetime.now()

response = requests.get(URL).json()

payload = {
    "fetched_at": fetched_at.isoformat(),
    "data": response
}
with open("sample_response.json", "w") as f:
    json.dump(payload, f, indent=4)
