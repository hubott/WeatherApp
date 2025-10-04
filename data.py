import json
import datetime
import psycopg2
from pprint import pprint
import os
from dotenv import load_dotenv
load_dotenv()

with open("sample_response.json", "r") as f:
    payload = json.load(f)

response = payload['data']
fetched_at = datetime.datetime.fromisoformat(payload['fetched_at'])


conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    port=os.getenv('DB_PORT')
)


cur = conn.cursor()
print("Database connection established.")

query = """
INSERT INTO hourly_weather (
    fetched_at,
    forecast_time,
	clouds,
	dew_point,
    temperature,
	feels_like,
    humidity,
	pop,
	pressure,
	UVI,
	visibility,
	weather,
    wind_speed,
	wind_deg,
	wind_gust
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (fetched_at, forecast_time) DO UPDATE SET
    temperature = EXCLUDED.temperature,
    feels_like = EXCLUDED.feels_like
"""

for i in range(len(response['hourly'])):
    forecast_time = response['hourly'][i]['dt']
    forecast_time_utc = datetime.datetime.fromtimestamp(forecast_time, datetime.timezone.utc)
    forecast_time_local = forecast_time_utc.astimezone()  # Convert to local timezone
    clouds = response['hourly'][i]['clouds']
    dew_point = response['hourly'][i]['dew_point']
    feels_like = int(response['hourly'][i]['feels_like']) - 273.15  # Convert from Kelvin to Celsius
    humidity = response['hourly'][i]['humidity']
    pop = response['hourly'][i]['pop']
    pressure = response['hourly'][i]['pressure']
    temperature = int(response['hourly'][i]['temp']) - 273.15  # Convert from Kelvin to Celsius
    UVI = response['hourly'][i]['uvi']
    visibility = response['hourly'][i]['visibility']
    weather = response['hourly'][i]['weather'][0]['description']
    wind_speed = response['hourly'][i]['wind_speed']
    wind_deg = response['hourly'][i]['wind_deg']
    wind_gust = response['hourly'][i].get('wind_gust', None)


    values = (
        fetched_at,
        forecast_time_local,
        clouds,
        dew_point,
        temperature,
        feels_like,
        humidity,
        pop,
        pressure,
        UVI,
        visibility,
        weather,
        wind_speed,
        wind_deg,
        wind_gust
    )

    cur.execute(query, values)

conn.commit()
print("Data inserted successfully.")
cur.close()
conn.close()
print("Database connection closed.")
