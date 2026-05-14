print("STARTING PROGRAM...")

import requests

API_KEY = "GQw4IuzmqDPa67usVd6svftkaYKkN3nUgPcbLcT6"

url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2024-01-01&end_date=2024-01-07&api_key=(API_KEY)"


print("Sending request...")

response = requests.get(url)


data = response.json()

print("data.keys()")

asteroids = []

for date in data["near_earth_objects"]:
    for obj in data["near_earth_objects"][date]:
        asteroids.append({
            "id": obj["id"],
            "name": obj["name"],
            "hazardous": obj["is_potentially_hazardous_asteroid"]
        })

print(asteroids[:5])
import sqlite3

conn = sqlite3.connect("asteroids.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS asteroids (
    id INTEGER,
    name TEXT,
    magnitude FLOAT,
    hazardous BOOLEAN
)
""")

conn.commit()
for ast in asteroids:
    cursor.execute("INSERT INTO asteroids VALUES (?, ?, ?, ?)", 
                   (ast["id"], ast["name"], ast["magnitude"], ast["hazardous"]))


import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("asteroids.db")

st.title("🚀 NASA Asteroid Dashboard")

query = st.selectbox("Choose option", [
    "Show Data",
    "Count Approaches"
])

if query == "Show Data":
    df = pd.read_sql_query("SELECT * FROM close_approach LIMIT 10;", conn)
    st.dataframe(df)

elif query == "Count Approaches":
    df = pd.read_sql_query("""
        SELECT neo_reference_id, COUNT(*) as total
        FROM close_approach
        GROUP BY neo_reference_id
        LIMIT 10;
    """, conn)
    st.dataframe(df)
