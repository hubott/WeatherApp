from flask import Flask, jsonify
import pg8000
import os
from dotenv import load_dotenv
from flask_cors import CORS




app = Flask(__name__)
CORS(app)
load_dotenv()

conn = pg8000.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    port=os.getenv('DB_PORT')
)

@app.route("/api/hourly")
def get_hourly():
    cur = conn.cursor()
    cur.execute("SELECT * FROM hourly_weather ORDER BY forecast_time DESC LIMIT 48")
    rows = cur.fetchall()
    data = []
    last_fetched = None
    for row in rows:
        if last_fetched is None or row[1] > last_fetched:
            last_fetched = row[1]
        data.append({
            "forecast_time": row[2].isoformat(),
            "temperature": row[5],
            "feels_like": row[6],
            "humidity": row[7],
            "weather": row[12]
        })
    print(last_fetched.isoformat())
    print("Returning", len(data), "records. Last fetched:", last_fetched)
    return jsonify({"last_refreshed": last_fetched.isoformat(), "hourly": data})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
