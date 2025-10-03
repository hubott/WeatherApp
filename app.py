import requests
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')
melbourne_lat = 37.81
melbourne_lon = 144.96
URL = f'https://api.openweathermap.org/data/3.0/onecall?lat={melbourne_lat}&lon={melbourne_lon}&appid={API_KEY}'

response = requests.get(URL).json()
print(response)