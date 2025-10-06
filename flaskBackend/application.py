# application.py
from flask import Flask, jsonify
import pg8000, os
import os
from flask_cors import CORS
import logging



app = Flask(__name__)
CORS(app)
app.logger.setLevel(logging.INFO)

app.logger.info("Starting Flask app")

app.logger.info(f"DB_HOST={os.environ.get('DB_HOST')}")
app.logger.info(f"DB_USER={os.environ.get('DB_USER')}")



def get_conn():
    return pg8000.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        port=os.environ.get('DB_PORT')
    )



@app.route("/api/hourly")
def get_hourly():

    # Get a new connection for each request to avoid stale connections
    conn = get_conn()
    cur = conn.cursor()
    # Query the most recent 48 hours of data, ensuring they are in order by forecast_time
    cur.execute("SELECT * FROM hourly_weather ORDER BY fetched_at DESC, forecast_time ASC LIMIT 48")
    rows = cur.fetchall()
    data = []
    last_fetched = None
    #Append the appropriate that we want sent to our frontend
    for row in rows:
        if last_fetched is None or row[1] > last_fetched:
            last_fetched = row[1]
        data.append({
            "forecast_time": row[2].isoformat(),
            "temperature": row[5],
            "feels_like": row[6],
            "humidity": row[7],
            "weather": row[12],
            "icon": row[16]
        })
    # Return the data as JSON
    return jsonify({"last_refreshed": last_fetched.isoformat(), "hourly": data})

# A simple health check endpoint
@app.route("/")
def health():
    return "Flask app is running!"


# Expose the app as 'application' for Beanstalk's WSGI server
application = app
if __name__ == "__main__":
    application.run(host="0.0.0.0")

