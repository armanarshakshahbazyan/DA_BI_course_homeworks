import csv
import requests
from datetime import datetime, timedelta

access_key = 'bf45b692fda9bcab3d33527915ceb825'
BASE_URL = 'https://data.fixer.io/api/'  # Fixer API base
symbols = 'USD,EUR,GBP'  # or any currencies you need

# Prepare CSV file
with open('last_30_days_rates.csv', 'w', newline='') as csvfile:
    fieldnames = ['date'] + symbols.split(',')
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Loop over last 30 days
    for i in range(30):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        url = f'{BASE_URL}{date}'
        params = {'access_key': access_key, 'symbols': symbols}
        response = requests.get(url, params=params)
        data = response.json()

        if data['success']:
            row = {'date': date, **data['rates']}
            writer.writerow(row)
        else:
            print(f"Error fetching data for {date}: {data['error']['info']}")

print("Data saved to last_30_days_rates.csv")
