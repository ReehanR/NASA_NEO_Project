import requests
import sqlite3
from datetime import datetime

print("🔥 Script started")

API_KEY = "GQw4IuzmqDPa67usVd6svftkaYKkN3nUgPcbLcT6"

url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2024-01-01&end_date=2024-01-07&api_key={API_KEY}"

conn = sqlite3.connect("neo.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS asteroids (
    id INTEGER,
    name TEXT,
    absolute_magnitude_h REAL,
    estimated_diameter_min_km REAL,
    estimated_diameter_max_km REAL,
    is_potentially_hazardous_asteroid BOOLEAN
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS close_approach (
    neo_reference_id INTEGER,
    close_approach_date DATE,
    relative_velocity_kmph REAL,
    astronomical REAL,
    miss_distance_km REAL,
    miss_distance_lunar REAL,
    orbiting_body TEXT
)
""")

asteroids_data = []
close_approach_data = []

count = 0

while count < 10:
    print("🚀 Fetching data...")

    response = requests.get(url)
    print("Status:", response.status_code)

    data = response.json()

    for date in data['near_earth_objects']:
        print("📅 Date:", date)

        for asteroid in data['near_earth_objects'][date]:
            print("Asteroid:", asteroid['name'])

            asteroids_data.append((
                int(asteroid['id']),
                asteroid.get('name', 'unknown'),
                float(asteroid['absolute_magnitude_h']),
                float(asteroid['estimated_diameter']['kilometers']['estimated_diameter_min']),
                float(asteroid['estimated_diameter']['kilometers']['estimated_diameter_max']),
                asteroid['is_potentially_hazardous_asteroid']
            ))

            for close in asteroid['close_approach_data']:
                close_approach_data.append((
                    int(asteroid['id']),
                    datetime.strptime(close['close_approach_date'], "%Y-%m-%d"),
                    float(close['relative_velocity']['kilometers_per_hour']),
                    float(close['miss_distance']['astronomical']),
                    float(close['miss_distance']['kilometers']),
                    float(close['miss_distance']['lunar']),
                    close.get('orbiting_body', 'Earth')
                ))

                count += 1

                if count >= 10:
                    break

            if count >= 10:
                break

        if count >= 10:
            break

    url = data['links']['next']

cursor.executemany("INSERT INTO asteroids VALUES (?, ?, ?, ?, ?, ?)", asteroids_data)
cursor.executemany("INSERT INTO close_approach VALUES (?, ?, ?, ?, ?, ?, ?)", close_approach_data)

conn.commit()
conn.close()

print("✅ Data Stored Successfully!")