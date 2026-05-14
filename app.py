import streamlit as st
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

# Page settings
st.set_page_config(page_title="NASA Dashboard", layout="wide")

# Title
st.title("🚀 NASA Asteroid Dashboard")
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: white;
    }

    h1, h2, h3 {
        color: #00d4ff;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Menu
menu = st.sidebar.selectbox(
    "Choose Option",
    [
        "Dashboard",
        "Hazardous Asteroids",
        "Fastest Asteroids"
    ]
)

# Database connection
conn = sqlite3.connect("neo.db")

# Metrics
total_asteroids = pd.read_sql_query(
    "SELECT COUNT(*) as total FROM asteroids", conn
)

hazardous = pd.read_sql_query(
    "SELECT COUNT(*) as hazardous FROM asteroids WHERE is_potentially_hazardous_asteroid = 1",
    conn
)

# Metric cards
col1, col2 = st.columns(2)

with col1:
    st.metric("☄️ Total Asteroids", total_asteroids['total'][0])

with col2:
    st.metric("⚠️ Hazardous", hazardous['hazardous'][0])
# Date Filter
st.subheader("📅 Filter By Close Approach Date")

date_query = pd.read_sql_query("""
SELECT DISTINCT close_approach_date
FROM close_approach
ORDER BY close_approach_date
""", conn)

date_list = date_query['close_approach_date'].tolist()

selected_date = st.selectbox(
    "Choose Date",
    date_list

)

# Show asteroid table
st.subheader("🪐 Asteroid Data")

df = pd.read_sql_query(f"""
SELECT a.*
FROM asteroids a
JOIN close_approach c
ON a.id = CAST(c.neo_reference_id AS INTEGER)
WHERE DATE(c.close_approach_date) = DATE('{selected_date}')
LIMIT 50
""", conn)

st.dataframe(df, use_container_width=True)

# Search feature
st.subheader("🔍 Search Asteroid")

search = st.text_input("Enter asteroid name")

if search:
    query = f"""
    SELECT * FROM asteroids
    WHERE name LIKE '%{search}%'
    LIMIT 50
    """

    search_df = pd.read_sql_query(query, conn)

    st.dataframe(search_df, use_container_width=True)

# Hazardous Asteroids
if menu == "Hazardous Asteroids":

    st.subheader("☠️ Hazardous Asteroids")

    hazardous_df = pd.read_sql_query("""
    SELECT name,
    is_potentially_hazardous_asteroid
    FROM asteroids
    WHERE is_potentially_hazardous_asteroid = 1
    """, conn)

    st.dataframe(hazardous_df, use_container_width=True)

# Fastest Asteroids
if menu == "Fastest Asteroids":

    st.subheader("⚡ Top 10 Fastest Asteroids")

    fastest_df = pd.read_sql_query("""
    SELECT neo_reference_id,
    relative_velocity_kmph
    FROM close_approach
    ORDER BY relative_velocity_kmph DESC
    LIMIT 10
    """, conn)

    st.dataframe(fastest_df, use_container_width=True)

# Chart
st.subheader("📊 Hazardous vs Non-Hazardous")

chart_data = pd.read_sql_query("""
SELECT is_potentially_hazardous_asteroid,
COUNT(*) as count
FROM asteroids
GROUP BY is_potentially_hazardous_asteroid
""", conn)

st.bar_chart(
    chart_data.set_index(
        'is_potentially_hazardous_asteroid'
    )
)

# Pie Chart
st.subheader("🥧 Hazardous Distribution")

pie_data = chart_data.set_index(
    'is_potentially_hazardous_asteroid'
)

st.pyplot(
    pie_data.plot.pie(
        y='count',
        autopct='%1.1f%%',
        figsize=(5, 5)
    ).figure
)

# Miss Distance Analytics
st.subheader("🌍 Closest Asteroids To Earth")

distance_df = pd.read_sql_query("""
SELECT neo_reference_id,
miss_distance_km,
miss_distance_lunar
FROM close_approach
ORDER BY miss_distance_km ASC
LIMIT 10
""", conn)

st.dataframe(distance_df, use_container_width=True)

# Distance Chart
st.line_chart(
    distance_df.set_index('neo_reference_id')[
        ['miss_distance_km']
    ]
)

# Fastest Asteroids Graph
st.subheader("⚡ Top 10 Fastest Asteroids")

fast_df = pd.read_sql_query("""
SELECT neo_reference_id,
relative_velocity_kmph
FROM close_approach
ORDER BY relative_velocity_kmph DESC
LIMIT 10
""", conn)

st.dataframe(fast_df, use_container_width=True)

# Bar Chart
st.bar_chart(
    fast_df.set_index('neo_reference_id')
)

# Close Database
conn.close()

# Bar Chart
st.bar_chart(
    fast_df.set_index('neo_reference_id')
)

# Close Database
conn.close()