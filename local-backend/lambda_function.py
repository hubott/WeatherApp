import requests
import os
import json
import datetime
import pg8000
from datetime import timedelta



def lambda_handler(event, context):
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
    cities = ["Melbourne", "Sydney"]
    cur = conn.cursor()
    API_KEY = os.environ['OPENWEATHER_API_KEY']
    

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
        wind_gust,
        icon_id,
        city
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (fetched_at, forecast_time) DO UPDATE SET
        temperature = EXCLUDED.temperature,
        feels_like = EXCLUDED.feels_like
    """

    for city in cities:
        Coords_URL = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={API_KEY}"
        coordReponse = requests.get(Coords_URL).json()

        if not coord_response:
            print(f"Skipping city {cityName}: no coordinates found")
            continue

        lat = coordReponse[0]['lat']
        lon = coordReponse[0]['lon']

        URL = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
        response = requests.get(URL).json()

        offset = response['timezone_offset']

        fetched_at = datetime.datetime.now()
        fetched_at = fetched_at + timedelta(seconds=offset)

        for i in range(len(response['hourly'])):
            forecast_time = response['hourly'][i]['dt']
            forecast_time = datetime.datetime.fromtimestamp(forecast_time, datetime.timezone.utc)
            forecast_time = forecast_time + timedelta(seconds=offset)
            clouds = response['hourly'][i]['clouds']
            dew_point = response['hourly'][i]['dew_point']
            feels_like = response['hourly'][i]['feels_like']
            humidity = response['hourly'][i]['humidity']
            pop = response['hourly'][i]['pop']
            pressure = response['hourly'][i]['pressure']
            temperature = response['hourly'][i]['temp']
            UVI = response['hourly'][i]['uvi']
            visibility = response['hourly'][i]['visibility']
            weather = response['hourly'][i]['weather'][0]['description']
            wind_speed = response['hourly'][i]['wind_speed']
            wind_deg = response['hourly'][i]['wind_deg']
            wind_gust = response['hourly'][i].get('wind_gust', None)
            icon_id = response['hourly'][i]['weather'][0]['icon']


            values = (
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
                wind_gust,
                icon_id,
                city
            )

            cur.execute(query, values)

    conn.commit()
    cur.close()
    conn.close()

    return {
        'statusCode': 200,
        'body': json.dumps('Weather data inserted successfully!')
    }