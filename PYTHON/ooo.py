import requests
import mysql.connector
from datetime import datetime, timedelta

# --- MySQL connection ---
conn = mysql.connector.connect(
    host="3.252.97.149",
    user="admin_remote",
    password="879dhJVBNwT)",
    database="RATE_GAE"
)
cursor = conn.cursor()

# --- Fixer API config (FREE plan) ---
API_KEY = "d9b9ab166d1db2a181b8a019f8621254"
BASE_URL = "https://data.fixer.io/api/"

# --- Date range: last 3 months ---
end_date = datetime.today()
start_date = end_date - timedelta(days=90)

# List of currencies
currencies = ["AMD", "USD", "EUR", "RUB"]

# Check if date already exists
def date_exists(date_str):
    cursor.execute(
        "SELECT COUNT(*) FROM exchange_rates WHERE rate_date = %s",
        (date_str,)
    )
    return cursor.fetchone()[0] > 0

current_date = start_date

while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")

    # Skip already loaded dates
    if date_exists(date_str):
        current_date += timedelta(days=1)
        continue

    # --- Daily API call (FREE plan allowed) ---
    response = requests.get(
        f"{BASE_URL}{date_str}",
        params={
            "access_key": API_KEY,
            "symbols": ",".join(currencies)
        }
    )

    data = response.json()

    if not data.get("success"):
        print(f"Skipped {date_str} (API error)")
        current_date += timedelta(days=1)
        continue

    rates = data["rates"]

    # --- Insert 4 rows per date ---
    for base in currencies:
        row = [date_str, base]

        for target in currencies:
            if base == target:
                row.append(1.0)
            else:
                row.append(rates[target] / rates[base])

        cursor.execute(
            """
            INSERT INTO exchange_rates
            (rate_date, base, AMD, USD, EUR, RUB)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            tuple(row)
        )

    conn.commit()
    print(f"Inserted 4 rows for {date_str}")

    current_date += timedelta(days=1)

cursor.close()
conn.close()
print("DONE ✅")
