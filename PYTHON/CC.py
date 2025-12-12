import requests
import pandas as pd
import mysql.connector

# -------------------------
# 1. Fetch data from API
# -------------------------
access_key = 'f86f57a6a509030ee4107d97687335c48'
BASE_URL = 'https://api.aviationstack.com/v1/flights'
params = {'access_key': access_key}

response = requests.get(BASE_URL, params=params)
data = response.json()

flights = data.get("data", [])

# Convert to DataFrame
df = pd.DataFrame(flights)

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
# 3. Create table (simple example)
# Adjust datatypes as needed
# -------------------------
create_table_query = """
CREATE TABLE IF NOT EXISTS flights (
    flight_date VARCHAR(50),
    flight_status VARCHAR(50),
    departure JSON,
    arrival JSON,
    airline JSON,
    flight JSON,
    aircraft JSON,
    live JSON
);
"""

cursor.execute(create_table_query)

# -------------------------
# 4. Insert data row by row
# -------------------------
insert_query = """
INSERT INTO flights (flight_date, flight_status, departure, arrival, airline, flight, aircraft, live)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():
    cursor.execute(
        insert_query,
        (
            row.get("flight_date"),
            row.get("flight_status"),
            str(row.get("departure")),
            str(row.get("arrival")),
            str(row.get("airline")),
            str(row.get("flight")),
            str(row.get("aircraft")),
            str(row.get("live")),
        )
    )

connection.commit()
cursor.close()
connection.close()

print("Data inserted into MySQL successfully!")
print("API rows:", len(flights))
print("DF rows:", len(df))
