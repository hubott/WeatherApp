import requests
import os
import json
import datetime
import pg8000

DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_PORT = os.environ['DB_PORT']

conn = pg8000.connect(
host=DB_HOST,
database=DB_NAME,
user=DB_USER,
password=DB_PASSWORD,
port=DB_PORT
)
cur = conn.cursor()

def lambda_handler(event, context):
    API_KEY = os.environ['OPENWEATHER_API_KEY']
    cityName = "Melbourne"
    Coords = f"http://api.openweathermap.org/geo/1.0/direct?q={cityName}&appid={API_KEY}"
    coordReponse = requests.get(Coords).json()
    lat = coordReponse[0]['lat']
    lon = coordReponse[0]['lon']
    URL = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_KEY}'
    response = requests.get(URL).json()
    fetched_at = datetime.datetime.now()

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
        feels_like = response['hourly'][i]['feels_like'] - 273.15  # Convert from Kelvin to Celsius
        humidity = response['hourly'][i]['humidity']
        pop = response['hourly'][i]['pop']
        pressure = response['hourly'][i]['pressure']
        temperature = response['hourly'][i]['temp'] - 273.15  # Convert from Kelvin to Celsius
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
    cur.close()
    conn.close()

    return {
        'statusCode': 200,
        'body': json.dumps('Weather data inserted successfully!')
    }