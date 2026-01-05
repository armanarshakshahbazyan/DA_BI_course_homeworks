import requests
import mysql.connector
from datetime import datetime, timedelta


# --- MySQL connection ---
conn = mysql.connector.connect(
    host="3.252.97.149",
    user="admin_remote",
    password="879dhJVBNwT)",
    database="RATE_GA"
)
cursor = conn.cursor()

# --- Fixer API config ---
API_KEY = "307dbba4f646a97521756fb147ee6fc9"
BASE_URL = "https://data.fixer.io/api/timeseries"

# --- Determine date range: last 6 months ---
end_date = datetime.today()
start_date = end_date - timedelta(days=180)

start_str = start_date.strftime("%Y-%m-%d")
end_str = end_date.strftime("%Y-%m-%d")

# List of currencies
currencies = ["AMD", "USD", "EUR", "RUB"]

# Function to check if a date already exists in DB
def date_exists(date_str):
    cursor.execute("SELECT COUNT(*) FROM exchange_rates WHERE rate_date = %s", (date_str,))
    return cursor.fetchone()[0] > 0

# --- Fetch all rates from API in one call ---
params = {
    "access_key": API_KEY,
    "start_date": 2025-06-13,
    "end_date": ,
    "symbols": ",".join(currencies),
    "base": "EUR"  # Free plan requires EUR as base
}

response = requests.get(BASE_URL, params=params)
data = response.json()

if not data.get("success"):
    print("API Error:", data.get("error"))
    exit()

# --- Loop over each date ---
for date_str, rates in data["rates"].items():
    if date_exists(date_str):
        continue  # Skip already inserted dates

    # Insert 4 rows per date, one per base
    for base in currencies:
        row = [date_str, base]
        for target in currencies:
            if base == target:
                row.append(1.0)
            else:
                # Convert rates to current base
                row.append(rates[target] / rates[base])
        # Insert row into DB
        cursor.execute(
            "INSERT INTO exchange_rates (rate_date, base, AMD, USD, EUR, RUB) VALUES (%s, %s, %s, %s, %s, %s)",
            tuple(row)
        )

    conn.commit()
    print(f"Inserted 4 recalculated rates for {date_str}")

cursor.close()
conn.close()
print("Done!")
