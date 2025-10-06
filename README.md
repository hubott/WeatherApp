# WeatherApp

A webapp that displays the current weather in Melbourne, as well as the temperature trends for the following 48 hours.
Future features: Trends for other stats, other cities

## Access

This project is deployed on AWS using: 
- RDS for the postgresql database
- Lambda for the API call and uploading to the database
- Eventbridge Scheduler to ensure the Lambda function runs every hour
- ElasticBeanstalk to deploy the Flask API
- S3 bucket for the static website hosting

Access Points:
- Website: [WeatherApp Frontend](http://weather-app-frontend.s3-website-ap-southeast-2.amazonaws.com)
- API: [Flask API](http://weatherapp-env.eba-kfmvwpd7.ap-southeast-2.elasticbeanstalk.com/api)

The Flask API returns the next 48 hours of weather data

**Response Example**

<pre>
{
  "hourly": [
    {
      "feels_like": 17.9,
      "forecast_time": "2025-10-06T22:00:00",
      "humidity": 65,
      "icon": "01d",
      "temperature": 18.4,
      "weather": "clear sky"
    },
    {
      "feels_like": 17.2,
      "forecast_time": "2025-10-06T18:00:00",
      "humidity": 67,
      "icon": "02d",
      "temperature": 17.8,
      "weather": "few clouds"
    },
    ...
  ],
  "last_refreshed":"2025-10-06T22:11:49.784428"
}
</pre>
