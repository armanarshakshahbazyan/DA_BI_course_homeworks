import requests
import pandas as pd
import mysql.connector

# -------------------------
# 1. Fetch data
# -------------------------
BASE_URL = "https://opensky-network.org/api/states/all"
response = requests.get(BASE_URL)
data = response.json()

states = data.get("states", [])

columns = [
    "icao24", "callsign", "origin_country", "time_position",
    "last_contact", "longitude", "latitude", "baro_altitude",
    "on_ground", "velocity", "true_track", "vertical_rate",
    "sensors", "geo_altitude", "squawk", "spi", "position_source"
]

# Convert each flight list to dictionary
flights_dicts = []
for s in states:
    flight = dict(zip(columns, s))
    flights_dicts.append(flight)

# Convert to DataFrame
df = pd.DataFrame(flights_dicts)

print("API rows:", len(df))
print("Columns:", df.columns)

# -------------------------
# 2. Connect to MySQL
# -------------------------
connection = mysql.connector.connect(
    host="3.252.97.149",
    user="admin_remote",
    password="879dhJVBNwT)",
    database="aviation_db"
)
cursor = connection.cursor()

# -------------------------
# 3. Reset table
# -------------------------
cursor.execute("DROP TABLE IF EXISTS flights;")

cursor.execute("""
CREATE TABLE flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    icao24 VARCHAR(10),
    callsign VARCHAR(20),
    origin_country VARCHAR(100),
    longitude DOUBLE,
    latitude DOUBLE,
    altitude DOUBLE,
    velocity DOUBLE,
    on_ground BOOLEAN
);
""")

# -------------------------
# 4. Insert data safely
# -------------------------
insert_query = """
INSERT INTO flights (
    icao24, callsign, origin_country,
    longitude, latitude, altitude,
    velocity, on_ground
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

rows = 0
for _, row in df.iterrows():
    cursor.execute(
        insert_query,
        (
            row["icao24"],
            row["callsign"].strip() if isinstance(row["callsign"], str) else None,
            row["origin_country"],
            row["longitude"] if row["longitude"] is not None else 0,
            row["latitude"] if row["latitude"] is not None else 0,
            row["geo_altitude"] if row["geo_altitude"] is not None else 0,
            row["velocity"] if row["velocity"] is not None else 0,
            row["on_ground"] if row["on_ground"] is not None else False,
        )
    )
    rows += 1

connection.commit()
cursor.close()
connection.close()

print("Rows inserted:", rows)
print("DONE ✅")
